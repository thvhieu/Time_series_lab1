from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import normaltest
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.seasonal import seasonal_decompose

PERIOD = 12
ALPHA = 0.05


def locate_dataset(base_dir: Path) -> Path:
    candidates = [
        base_dir.parent / "data" / "raw" / "AirPassengers.csv",
        base_dir / "AirPassengers.csv",
        base_dir / "data" / "raw" / "AirPassengers.csv",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    tried = "\n".join(f"  - {p}" for p in candidates)
    raise FileNotFoundError(
        f"Không tìm thấy AirPassengers.csv. Hãy đặt file tại một trong các vị trí:\n{tried}\nCSV phải có hai cột 'date' và 'value'."
    )


def load_series(path: Path) -> pd.Series:
    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]

    date_col = next((c for c in ("date", "month", "ds") if c in df.columns), None)
    value_col = next((c for c in ("value", "passengers", "y") if c in df.columns), None)
    if date_col is None or value_col is None:
        raise ValueError(f"CSV cần có cột ngày và giá trị. Các cột đang có: {list(df.columns)}")

    df = df[[date_col, value_col]].copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    df = df.dropna(subset=[date_col, value_col]).sort_values(date_col)

    if df.empty:
        raise ValueError("Dataset không có dòng dữ liệu hợp lệ.")
    if df[date_col].duplicated().any():
        duplicates = df.loc[df[date_col].duplicated(), date_col].astype(str).tolist()
        raise ValueError(f"Có ngày bị trùng, cần xử lý trước khi phân rã: {duplicates[:5]}")
    if (df[value_col] <= 0).any():
        raise ValueError("Mô hình Multiplicative yêu cầu mọi giá trị quan sát phải dương.")

    ts = df.set_index(date_col)[value_col].astype(float)
    ts.index.name = "date"

    ts.index = ts.index.to_period("M").to_timestamp()
    if ts.index.duplicated().any():
        raise ValueError("Có nhiều bản ghi cùng tháng sau khi chuẩn hóa. Hãy tổng hợp về một giá trị/tháng.")
    full_index = pd.date_range(ts.index.min(), ts.index.max(), freq="MS")
    ts = ts.reindex(full_index)
    ts.index.name = "date"

    if ts.isna().any():
        missing = ts[ts.isna()].index.strftime("%Y-%m").tolist()
        raise ValueError(f"Chuỗi có tháng bị thiếu: {missing[:12]}")
    if len(ts) < 2 * PERIOD:
        raise ValueError(f"Cần tối thiểu {2 * PERIOD} quan sát cho phân rã mùa vụ chu kỳ {PERIOD}; hiện có {len(ts)}.")
    return ts


def safe_float(value: Any) -> float | None:
    try:
        number = float(value)
        return number if np.isfinite(number) else None
    except (TypeError, ValueError):
        return None


def analyze(ts: pd.Series, output_dir: Path, base_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)

    decomp = seasonal_decompose(
        ts, model="multiplicative", period=PERIOD, extrapolate_trend="freq"
    )

    results = pd.DataFrame({
        "Observed": decomp.observed,
        "Trend": decomp.trend,
        "Seasonal": decomp.seasonal,
        "Residual": decomp.resid,
    }, index=ts.index)
    results.index.name = "date"
    results.to_csv(output_dir / "decomposition_results.csv", float_format="%.6f")

    seasonal_table = pd.DataFrame({
        "month": np.arange(1, 13),
        "month_name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "seasonal_index": decomp.seasonal.groupby(decomp.seasonal.index.month).mean().reindex(range(1, 13)).values,
    })
    seasonal_table["deviation_percent"] = (seasonal_table["seasonal_index"] - 1) * 100
    seasonal_table.to_csv(output_dir / "monthly_seasonal_indices.csv", index=False, float_format="%.6f")

    trend = decomp.trend.dropna()
    trend_start, trend_end = float(trend.iloc[0]), float(trend.iloc[-1])
    total_change_pct = (trend_end / trend_start - 1) * 100 if trend_start else np.nan
    elapsed_years = (trend.index[-1] - trend.index[0]).days / 365.2425
    cagr_pct = ((trend_end / trend_start) ** (1 / elapsed_years) - 1) * 100 if elapsed_years > 0 and trend_start > 0 else np.nan

    x = np.arange(len(trend), dtype=float)
    y = trend.to_numpy(dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    fitted = slope * x + intercept
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r_squared = 1 - float(np.sum((y - fitted) ** 2)) / ss_tot if ss_tot > 0 else np.nan

    sidx = seasonal_table.set_index("month")["seasonal_index"]
    peak_month = int(sidx.idxmax())
    trough_month = int(sidx.idxmin())
    seasonal_range_pct = (float(sidx.max()) / float(sidx.min()) - 1) * 100

    log_ts = np.log(ts)
    log_decomp = seasonal_decompose(
        log_ts, model="additive", period=PERIOD, extrapolate_trend="freq"
    )
    log_resid = log_decomp.resid.dropna()
    common_index = log_resid.index
    var_resid = float(np.nanvar(log_decomp.resid))
    var_trend_plus_resid = float(np.nanvar((log_decomp.trend + log_decomp.resid).loc[common_index]))
    var_seasonal_plus_resid = float(np.nanvar((log_decomp.seasonal + log_decomp.resid).loc[common_index]))
    trend_strength = max(0.0, 1 - var_resid / var_trend_plus_resid) if var_trend_plus_resid > 0 else np.nan
    seasonal_strength = max(0.0, 1 - var_resid / var_seasonal_plus_resid) if var_seasonal_plus_resid > 0 else np.nan

    residual = decomp.resid.dropna()
    residual_centered = residual - 1.0
    lb_lags = [lag for lag in (12, 24) if lag < len(residual_centered)]
    lb_results = acorr_ljungbox(residual_centered, lags=lb_lags, return_df=True) if lb_lags else pd.DataFrame()
    lb_pvalues = {str(int(lag)): safe_float(row["lb_pvalue"]) for lag, row in lb_results.iterrows()}
    white_noise_at_12 = None
    if "12" in lb_pvalues and lb_pvalues["12"] is not None:
        white_noise_at_12 = bool(lb_pvalues["12"] > ALPHA)

    residual_mean = float(residual_centered.mean())
    residual_std = float(residual_centered.std(ddof=1))
    residual_acf1 = float(residual_centered.autocorr(lag=1)) if len(residual_centered) > 1 else np.nan
    normality_pvalue = None
    if len(residual_centered) >= 8:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            normality_pvalue = safe_float(normaltest(residual_centered).pvalue)

    summary = {
        "dataset": "AirPassengers",
        "observations": int(len(ts)),
        "start": ts.index.min().strftime("%Y-%m-%d"),
        "end": ts.index.max().strftime("%Y-%m-%d"),
        "period": PERIOD,
        "model": "multiplicative classical decomposition",
        "trend_start": safe_float(trend_start),
        "trend_end": safe_float(trend_end),
        "trend_total_change_percent": safe_float(total_change_pct),
        "trend_cagr_percent": safe_float(cagr_pct),
        "trend_linear_slope_per_month": safe_float(slope),
        "trend_linear_r_squared": safe_float(r_squared),
        "trend_strength": safe_float(trend_strength),
        "seasonal_strength": safe_float(seasonal_strength),
        "seasonal_peak_month": peak_month,
        "seasonal_trough_month": trough_month,
        "seasonal_peak_index": safe_float(sidx.max()),
        "seasonal_trough_index": safe_float(sidx.min()),
        "seasonal_peak_to_trough_change_percent": safe_float(seasonal_range_pct),
        "residual_centered_mean": safe_float(residual_mean),
        "residual_centered_std": safe_float(residual_std),
        "residual_acf_lag1": safe_float(residual_acf1),
        "ljung_box_pvalues": lb_pvalues,
        "white_noise_at_lag12_alpha_005": white_noise_at_12,
        "normality_test_pvalue": normality_pvalue,
        "alpha": ALPHA,
    }
    (output_dir / "analysis_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    plot_specs = [
        (decomp.observed, "Observed — Dữ liệu quan sát", "#1f77b4"),
        (decomp.trend, "Trend — Xu hướng dài hạn", "#ff7f0e"),
        (decomp.seasonal, "Seasonal — Mùa vụ (chu kỳ 12 tháng)", "#2ca02c"),
        (decomp.resid, "Residual — Phần dư (tâm tham chiếu = 1)", "#d62728"),
    ]
    for ax, (series, title, color) in zip(axes, plot_specs):
        ax.plot(series.index, series.values, color=color, linewidth=1.35)
        ax.set_title(title, fontsize=10, loc="left")
        ax.grid(True, linestyle="--", alpha=0.35)
    axes[3].axhline(1, color="black", linestyle="--", linewidth=1, alpha=0.7)
    axes[3].set_xlabel("Date")
    fig.suptitle("AirPassengers — Classical Multiplicative Decomposition", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(output_dir / "decomposition_plot.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(11, 7))
    axes[0].plot(residual_centered.index, residual_centered.values, color="#d62728", linewidth=1.2)
    axes[0].axhline(0, color="black", linestyle="--", linewidth=1)
    axes[0].set_title("Residual đã trừ 1 (dao động quanh 0)")
    axes[0].grid(True, linestyle="--", alpha=0.35)
    plot_acf(residual_centered, lags=min(36, max(1, len(residual_centered) // 2 - 1)), ax=axes[1], zero=False)
    axes[1].set_title("ACF của residual đã trừ 1")
    axes[1].grid(True, linestyle="--", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "residual_diagnostics.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(seasonal_table["month_name"], seasonal_table["seasonal_index"], color="#2ca02c", alpha=0.8)
    ax.axhline(1, color="black", linestyle="--", linewidth=1, label="Mức trung tính = 1")
    ax.set_title("Monthly Seasonal Indices — Multiplicative Model")
    ax.set_ylabel("Seasonal index")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "seasonal_pattern.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    month_names = seasonal_table.set_index("month")["month_name"].to_dict()
    trend_direction = "tăng" if slope > 0 else ("giảm" if slope < 0 else "gần như đi ngang")
    if white_noise_at_12 is True:
        white_noise_text = (
            "Ở mức ý nghĩa 5%, chưa có đủ bằng chứng bác bỏ giả thuyết không có tự tương quan "
            "đến độ trễ 12 (Ljung–Box). Điều này phù hợp với white noise theo kiểm định này."
        )
    elif white_noise_at_12 is False:
        white_noise_text = (
            "Kiểm định Ljung–Box tại độ trễ 12 có p-value ≤ 0,05; bác bỏ giả thuyết không có "
            "tự tương quan. Residual chưa thể xem là white noise."
        )
    else:
        white_noise_text = "Không đủ điều kiện tính kiểm định Ljung–Box tại độ trễ 12."

    report = f"""# Báo cáo phân rã chuỗi thời gian AirPassengers

## 1. Phương pháp

Sử dụng **classical multiplicative decomposition** với chu kỳ mùa vụ `period = {PERIOD}` tháng. Mô hình:

\\[Y_t = T_t \\times S_t \\times R_t\\]

Dữ liệu có **{len(ts)} quan sát tháng**, từ **{ts.index.min():%Y-%m}** đến **{ts.index.max():%Y-%m}**. Biểu đồ phân rã lưu tại `output/decomposition_plot.png`.

## 2. Kết quả

### 2.1. Xu hướng (Trend)
- Trend đầu kỳ: **{trend_start:.2f}**; cuối kỳ: **{trend_end:.2f}**.
- Thay đổi tổng cộng: **{total_change_pct:.2f}%** (CAGR: **{cagr_pct:.2f}%/năm**).
- Độ dốc tuyến tính: **{slope:.4f} đơn vị/tháng** (R² = **{r_squared:.4f}**).
- Độ mạnh xu hướng: **{trend_strength:.4f}**.
- Kết luận: xu hướng tổng quát **{trend_direction}**.

### 2.2. Mùa vụ (Seasonal)
- Tháng đỉnh mùa vụ: **{month_names[peak_month]}** (index = **{float(sidx.max()):.4f}**).
- Tháng đáy mùa vụ: **{month_names[trough_month]}** (index = **{float(sidx.min()):.4f}**).
- Chênh lệch đỉnh/đáy: **{seasonal_range_pct:.2f}%**.
- Độ mạnh mùa vụ: **{seasonal_strength:.4f}**.

### 2.3. Phần dư (Residual) và white noise
- Trung bình của `Residual - 1`: **{residual_mean:.5f}**.
- Độ lệch chuẩn của `Residual - 1`: **{residual_std:.5f}**.
- ACF tại độ trễ 1: **{residual_acf1:.4f}**.
- p-value Ljung–Box: **{json.dumps(lb_pvalues, ensure_ascii=False)}**.
- {white_noise_text}

## 3. Nhận xét
1. **Xu hướng:** {trend_direction.capitalize()} rõ nét theo thời gian.
2. **Mùa vụ:** Mùa vụ {'mạnh' if seasonal_strength >= 0.6 else 'trung bình'} với đỉnh vào {month_names[peak_month]} và đáy vào {month_names[trough_month]}.
3. **Residual:** {('chưa có bằng chứng tự tương quan đáng kể tại lag 12' if white_noise_at_12 is True else 'còn tồn tại tự tương quan tại lag 12')}.

## Danh mục tệp đầu ra
- `report.md`: Báo cáo phương pháp, kết quả và nhận xét.
- `output/decomposition_results.csv`: Dữ liệu phân rã chi tiết.
- `output/monthly_seasonal_indices.csv`: Chỉ số mùa vụ theo từng tháng.
- `output/decomposition_plot.png`: Biểu đồ 4 thành phần.
- `output/residual_diagnostics.png`: Đồ thị phân tích phần dư và ACF.
- `output/seasonal_pattern.png`: Biểu đồ cột chỉ số mùa vụ.
- `output/analysis_summary.json`: Tóm tắt các chỉ số thống kê.
"""
    (base_dir / "report.md").write_text(report, encoding="utf-8")
    return summary


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    dataset_path = locate_dataset(base_dir)
    output_dir = base_dir / "output"

    print(f"[*] Đang đọc dữ liệu: {dataset_path}")
    ts = load_series(dataset_path)
    print(f"[*] Số quan sát: {len(ts)} | từ {ts.index.min():%Y-%m} đến {ts.index.max():%Y-%m}")
    summary = analyze(ts, output_dir, base_dir)

    print("\n" + "=" * 64)
    print("TÓM TẮT KẾT QUẢ PHÂN RÃ")
    print("=" * 64)
    print(f"- Trend: {summary['trend_start']:.2f} -> {summary['trend_end']:.2f}")
    print(f"- Mức thay đổi Trend: {summary['trend_total_change_percent']:.2f}%")
    print(f"- CAGR Trend: {summary['trend_cagr_percent']:.2f}%/năm")
    print(f"- Độ mạnh Trend: {summary['trend_strength']:.4f}")
    print(f"- Độ mạnh Seasonal: {summary['seasonal_strength']:.4f}")
    print(f"- Tháng đỉnh mùa vụ: {summary['seasonal_peak_month']}")
    print(f"- Tháng đáy mùa vụ: {summary['seasonal_trough_month']}")
    print(f"- Ljung–Box p-values: {summary['ljung_box_pvalues']}")
    print(f"- White noise tại lag 12 (alpha=0.05): {summary['white_noise_at_lag12_alpha_005']}")
    print(f"\n[✓] Đã tạo report.md tại thư mục hiện tại")
    print(f"[✓] Đã lưu các kết quả và biểu đồ tại: {output_dir}")


if __name__ == "__main__":
    main()