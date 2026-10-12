"""Người 1: kiểm tra và xử lý chất lượng dữ liệu."""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "..", "data", "raw", "AirPassengers.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def load_data():
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(INPUT_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.sort_values("date").reset_index(drop=True)
    return df


def check_data_quality(df):
    # Kiểm tra thông tin dữ liệu
    print("\n===== THÔNG TIN DỮ LIỆU =====")
    df.info()

    print("\n===== 5 DÒNG ĐẦU =====")
    print(df.head())

    print("\n===== KIỂM TRA GIÁ TRỊ THIẾU =====")
    print(df.isna().sum())

    print("\n===== KIỂM TRA DỮ LIỆU TRÙNG =====")
    print("Số dòng trùng:", df.duplicated().sum())
    print("Số ngày trùng:", df["date"].duplicated().sum())

    print("\n===== KIỂU DỮ LIỆU =====")
    print(df.dtypes)


def create_missing_data(df):
    # Tạo dữ liệu missing bằng cách đặt một số giá trị thành NaN
    missing_df = df.copy()

    # Chọn 1 số vị trí để tạo dữ liệu missing (NaN)
    missing_indices = [10, 25, 40, 70, 100, 120]
    missing_df.loc[missing_indices, "value"] = np.nan
    missing_df.to_csv(
        os.path.join(OUTPUT_DIR, "missing_data.csv"),
        index=False
    )

    print("\n===== DỮ LIỆU SAU KHI TẠO MISSING =====")
    print(missing_df.isna().sum())
    
    return missing_df


def handle_missing_data(df):
    # Xử lý missing bằng Forward-fill và Interpolation
    # Forward-fill
    ffill_df = df.copy()
    ffill_df["value"] = ffill_df["value"].ffill()

    # Interpolation
    interpolation_df = df.copy()
    interpolation_df["value"] = interpolation_df["value"].interpolate(
        method="linear"
    )

    ffill_df.to_csv(
        os.path.join(OUTPUT_DIR, "missing_ffill.csv"),
        index=False
    )

    interpolation_df.to_csv(
        os.path.join(OUTPUT_DIR, "missing_interpolation.csv"),
        index=False
    )

    print("\n===== SAU KHI FILL MISSING =====")
    print("Forward-fill:", ffill_df["value"].isna().sum(), "giá trị thiếu")
    print("Interpolation:", interpolation_df["value"].isna().sum(), "giá trị thiếu")

    return ffill_df, interpolation_df


def plot_missing_comparison(original_df, missing_df, ffill_df, interpolation_df):
    plt.figure(figsize=(14, 6))

    plt.plot(
        original_df["date"],
        original_df["value"],
        label="Dữ liệu gốc",
        color="blue"
    )

    # Đánh dấu vị trí dữ liệu bị thiếu trên dữ liệu gốc
    missing_mask = missing_df["value"].isna()

    plt.scatter(
        original_df.loc[missing_mask, "date"],
        original_df.loc[missing_mask, "value"],
        label="Vị trí missing",
        marker="x",
        s=70,
        color="red"
    )

    plt.plot(
        ffill_df["date"],
        ffill_df["value"],
        label="Forward-fill",
        linestyle="--"
    )

    plt.plot(
        interpolation_df["date"],
        interpolation_df["value"],
        label="Interpolation",
        linestyle=":"
    )

    plt.title("So sánh dữ liệu trước và sau khi xử lý missing")
    plt.xlabel("Thời gian")
    plt.ylabel("Số lượng hành khách")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "missing_comparison.png")
    )
    plt.show()


def detect_outliers(df):
    # Phát hiện outlier bằng Z-score và rolling mean/variance
    result = df.copy()

    # Tính rolling mean và rolling variance
    result["rolling_mean"] = (
        result["value"]
        .rolling(window=12)
        .mean()
    )

    result["rolling_var"] = (
        result["value"]
        .rolling(window=12)
        .var()
    )

    result["rolling_std"] = (
        result["value"]
        .rolling(window=12)
        .std()
    )

    # Phát hiện outlier bằng Z-score
    mean_value = result["value"].mean()
    std_value = result["value"].std()
    result["z_score"] = (
        (result["value"] - mean_value) / std_value
    )

    # Xác định outlier dựa trên Z-score > 3 hoặc < -3
    result["is_outlier"] = result["z_score"].abs() > 3
    result.to_csv(
        os.path.join(OUTPUT_DIR, "outliers.csv"),
        index=False
    )

    print("\n===== KẾT QUẢ PHÁT HIỆN OUTLIER =====")
    print("Số lượng outlier:", result["is_outlier"].sum())
    print(result.loc[result["is_outlier"], ["date", "value", "z_score"]])

    return result


def plot_outliers(result):
    # Vẽ biểu đồ dữ liệu gốc, rolling mean và outlier
    plt.figure(figsize=(14, 6))

    plt.plot(
        result["date"],
        result["value"],
        label="Dữ liệu gốc"
    )

    plt.plot(
        result["date"],
        result["rolling_mean"],
        label="Rolling mean (12 tháng)",
        linestyle="--"
    )

    outliers = result[result["is_outlier"]]

    plt.scatter(
        outliers["date"],
        outliers["value"],
        color="red",
        marker="x",
        s=70,
        label="Outliers"
    )

    plt.title("Phát hiện Outlier bằng Z-score và Rolling Mean")
    plt.xlabel("Thời gian")
    plt.ylabel("Số lượng hành khách")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "outlier_detection.png")
    )
    plt.show()


def main():
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Đọc dữ liệu
    df = load_data()

    # 2. Kiểm tra chất lượng dữ liệu
    check_data_quality(df)

    # 3. Tạo dữ liệu missing
    missing_df = create_missing_data(df)

    # 4. Xử lý missing bằng Forward-fill và Interpolation
    ffill_df, interpolation_df = handle_missing_data(missing_df)

    # 5. Vẽ biểu đồ so sánh trước và sau xử lý missing
    plot_missing_comparison(df, missing_df, ffill_df, interpolation_df)

    # 6. Phát hiện outlier
    result = detect_outliers(df)

    # 7. Vẽ biểu đồ outlier
    plot_outliers(result)

if __name__ == "__main__":
    main()