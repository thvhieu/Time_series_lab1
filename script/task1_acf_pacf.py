"""Task 1: Tính và phân tích ACF/PACF đến 40 lags cho chuỗi dữ liệu AirPassengers.

Mục tiêu mã nguồn:
1. Tải và xem trước dữ liệu (head, info, describe, plot).
2. Tính toán và vẽ biểu đồ ACF, PACF đến 40 lags.
3. Xuất các artifact (hình ảnh .png và dữ liệu bảng .csv).
(Toàn bộ phân tích, nhận xét và kết luận chi tiết được trình bày tại report.md)
"""

import sys
from pathlib import Path

# Đảm bảo console Windows hỗ trợ in UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf


def get_project_paths() -> tuple[Path, Path]:
    """Xác định đường dẫn file dữ liệu đầu vào và thư mục lưu trữ output."""
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent

    data_path = project_root / "data" / "raw" / "AirPassengers.csv"
    if not data_path.exists():
        data_path = Path("data/raw/AirPassengers.csv")

    output_dir = current_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return data_path, output_dir


def load_and_preview_data(data_path: Path) -> pd.DataFrame:
    """Đọc dữ liệu và in thông tin cấu trúc xem trước (head, info, describe)."""
    print("=" * 60)
    print("1. TAI VA XEM TRUOC DU LIEU")
    print("=" * 60)

    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    print("\n--- 5 dong dau tien (head) ---")
    print(df.head())

    print("\n--- Thong tin cau truc (info) ---")
    df.info()

    print("\n--- Thong ke mo ta (describe) ---")
    print(df["value"].describe())
    return df


def plot_time_series(df: pd.DataFrame, output_dir: Path) -> Path:
    """Vẽ và lưu biểu đồ chuỗi thời gian gốc (plot)."""
    save_path = output_dir / "airpassengers_time_series.png"

    plt.figure(figsize=(10, 4.8), dpi=300)
    plt.plot(df["date"], df["value"], color="#1f77b4", linewidth=2, label="Monthly Passengers")
    plt.title("AirPassengers: Monthly Airline Passenger Numbers (1949 - 1960)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Year", fontsize=11)
    plt.ylabel("Number of Passengers (Thousands)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print(f"\n[Saved] Bieu do chuoi thoi gian: {save_path.name}")
    return save_path


def compute_and_save_lags(series: pd.Series, max_lags: int, output_dir: Path) -> pd.DataFrame:
    """Tính toán trị số ACF, PACF đến 40 lags và xuất ra file CSV."""
    acf_vals, acf_ci = acf(series, nlags=max_lags, alpha=0.05, result_object=False)
    pacf_vals, pacf_ci = pacf(series, nlags=max_lags, alpha=0.05)

    results_df = pd.DataFrame({
        "Lag": list(range(max_lags + 1)),
        "ACF": acf_vals,
        "ACF_CI_Lower": acf_ci[:, 0] - acf_vals,
        "ACF_CI_Upper": acf_ci[:, 1] - acf_vals,
        "PACF": pacf_vals,
        "PACF_CI_Lower": pacf_ci[:, 0] - pacf_vals,
        "PACF_CI_Upper": pacf_ci[:, 1] - pacf_vals,
    })

    csv_path = output_dir / "acf_pacf_values.csv"
    results_df.to_csv(csv_path, index=False)
    print(f"[Saved] Du lieu bang ACF/PACF: {csv_path.name}")
    return results_df


def plot_acf_pacf(series: pd.Series, max_lags: int, output_dir: Path) -> Path:
    """Vẽ và lưu biểu đồ ACF và PACF đến 40 lags."""
    save_path = output_dir / "acf_pacf_40lags.png"

    fig, axes = plt.subplots(2, 1, figsize=(11, 7.5), dpi=300)

    # 1. Đồ thị ACF
    plot_acf(series, lags=max_lags, ax=axes[0], color="#d62728", vlines_kwargs={"colors": "#d62728", "linewidth": 1.2})
    axes[0].set_title(f"Autocorrelation Function (ACF) - Up to {max_lags} Lags", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Lag", fontsize=10)
    axes[0].set_ylabel("ACF Coefficient", fontsize=10)
    axes[0].set_xticks(range(0, max_lags + 1, 2))
    axes[0].grid(True, linestyle="--", alpha=0.4)

    # Đánh dấu các mốc mùa vụ (lag 12, 24, 36)
    for season_lag in [12, 24, 36]:
        if season_lag <= max_lags:
            axes[0].axvline(x=season_lag, color="#2ca02c", linestyle=":", alpha=0.7)

    # 2. Đồ thị PACF
    plot_pacf(series, lags=max_lags, ax=axes[1], color="#1f77b4", method="ywm", vlines_kwargs={"colors": "#1f77b4", "linewidth": 1.2})
    axes[1].set_title(f"Partial Autocorrelation Function (PACF) - Up to {max_lags} Lags", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Lag", fontsize=10)
    axes[1].set_ylabel("PACF Coefficient", fontsize=10)
    axes[1].set_xticks(range(0, max_lags + 1, 2))
    axes[1].grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print(f"[Saved] Bieu do ACF & PACF 40 lags: {save_path.name}")
    return save_path


def main() -> None:
    # Xác định đường dẫn
    data_path, output_dir = get_project_paths()

    # 1. Tải và xem trước dữ liệu (head, info, plot)
    df = load_and_preview_data(data_path)
    plot_time_series(df, output_dir)

    # 2. Tính toán và vẽ biểu đồ ACF/PACF đến 40 lags (xuất CSV & PNG)
    compute_and_save_lags(df["value"], max_lags=40, output_dir=output_dir)
    plot_acf_pacf(df["value"], max_lags=40, output_dir=output_dir)

    print("\n" + "=" * 60)
    print("HOAN TAT: Du lieu va bieu do da duoc luu vao thu muc 'output/'.")
    print("Chi tiet nhan xet va phan tich ket luan xem tai file 'report.md'.")
    print("=" * 60)


if __name__ == "__main__":
    main()
