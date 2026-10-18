"""Bài tập 5: Trực quan hóa dữ liệu chuỗi thời gian."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "AirPassengers.csv"
OUT_DIR = Path(__file__).resolve().parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MONTH_NAMES = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    return df


# 1. Line chart toàn bộ chuỗi
def plot_line_chart(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df["date"], df["value"], color="#2563EB", linewidth=1.5,
            label="Hành khách thực tế")
    ax.set_title("Line Chart – Số hành khách hàng không quốc tế (1949–1960)")
    ax.set_xlabel("Thời gian")
    ax.set_ylabel("Số hành khách (nghìn)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "01_line_chart.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved: 01_line_chart.png")


# 2. Rolling mean (window=12) và rolling std
def plot_rolling_stats(df: pd.DataFrame) -> None:
    roll_mean = df["value"].rolling(window=12, center=True).mean()
    roll_std  = df["value"].rolling(window=12, center=True).std()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    ax1.plot(df["date"], df["value"], color="#94A3B8", linewidth=1, label="Thực tế")
    ax1.plot(df["date"], roll_mean, color="#F97316", linewidth=2, label="Rolling Mean (12)")
    ax1.set_title("Rolling Mean (window=12)")
    ax1.set_ylabel("Số hành khách (nghìn)")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.4)

    ax2.plot(df["date"], roll_std, color="#7C3AED", linewidth=2, label="Rolling Std (12)")
    ax2.set_title("Rolling Std (window=12)")
    ax2.set_ylabel("Độ lệch chuẩn")
    ax2.set_xlabel("Thời gian")
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.4)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "02_rolling_stats.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved: 02_rolling_stats.png")


# 3. Seasonal plot theo tháng
def plot_seasonal(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(3, 4, figsize=(14, 8), sharey=True)
    axes = axes.flatten()
    for m_idx, ax in enumerate(axes):
        month = m_idx + 1
        sub = df[df["month"] == month]
        ax.plot(sub["year"], sub["value"], marker="o", markersize=4,
                linewidth=1.5, color="#2563EB")
        ax.axhline(sub["value"].mean(), color="#DC2626", linewidth=1.2,
                   linestyle="--", alpha=0.8)
        ax.set_title(MONTH_NAMES[m_idx], fontsize=10, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.tick_params(labelsize=7)
    fig.suptitle("Seasonal Plot – Biến động từng tháng qua các năm (1949–1960)",
                 fontsize=12, fontweight="bold")
    fig.text(0.5, -0.01, "Năm", ha="center")
    fig.text(-0.01, 0.5, "Số hành khách (nghìn)", va="center", rotation="vertical")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "03_seasonal_plot.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved: 03_seasonal_plot.png")


# 4. Heatmap seasonality (month × year)
def plot_heatmap(df: pd.DataFrame) -> None:
    pivot = df.pivot_table(index="month", columns="year", values="value")

    fig, ax = plt.subplots(figsize=(12, 5))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd", origin="upper")

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, fontsize=9)
    ax.set_yticks(range(12))
    ax.set_yticklabels(MONTH_NAMES, fontsize=9)

    for i in range(12):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            color = "white" if val > pivot.values.max() * 0.65 else "black"
            ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                    fontsize=7, color=color, fontweight="bold")

    fig.colorbar(im, ax=ax, label="Số hành khách (nghìn)")
    ax.set_title("Heatmap Seasonality – Tháng × Năm", fontsize=12, fontweight="bold")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Tháng")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "04_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved: 04_heatmap.png")


def main() -> None:
    print("=== Bài tập 5: Trực quan hóa chuỗi thời gian ===")
    df = load_data()
    print(f"  Dữ liệu: {len(df)} quan sát ({df['date'].min().date()} → {df['date'].max().date()})\n")

    print("[1] Line chart toàn bộ chuỗi")
    plot_line_chart(df)

    print("[2] Rolling mean & rolling std (window=12)")
    plot_rolling_stats(df)

    print("[3] Seasonal plot theo tháng")
    plot_seasonal(df)

    print("[4] Heatmap seasonality (month × year)")
    plot_heatmap(df)

    print(f"\n✓ Xong! Biểu đồ lưu tại: {OUT_DIR}")


if __name__ == "__main__":
    main()
