"""Người 3: sinh và phân tích white noise."""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.datasets import get_rdataset

def main() -> None:
    # Tạo thư mục output nếu chưa có
    os.makedirs("output", exist_ok=True)

    # 1. Sinh dữ liệu white noise bằng NumPy (1000 điểm)
    np.random.seed(42)
    white_noise = np.random.normal(loc=0, scale=1, size=1000)

    # 2. Tải chuỗi dữ liệu AirPassengers để so sánh
    air_passengers = get_rdataset("AirPassengers").data
    ap_series = air_passengers['value']

    # 3. Vẽ biểu đồ ACF
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plot_acf(white_noise, lags=40, ax=plt.gca())
    plt.title("ACF - White Noise")

    plt.subplot(1, 2, 2)
    plot_acf(ap_series, lags=40, ax=plt.gca())
    plt.title("ACF - AirPassengers")

    plt.tight_layout()

    # Lưu biểu đồ vào thư mục output
    output_path = "output/acf_comparison.png"
    plt.savefig(output_path)
    plt.show()
    
    print(f"Đã chạy thành công! Biểu đồ được lưu tại {output_path}")

if __name__ == "__main__":
    main()
