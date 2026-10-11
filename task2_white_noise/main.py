"""Người 3: sinh và phân tích white noise."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.datasets import get_rdataset

# 1. Sinh dữ liệu white noise bằng NumPy (1000 điểm)
np.random.seed(42)
white_noise = np.random.normal(loc=0, scale=1, size=1000)

# 2. Vẽ ACF của White Noise
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plot_acf(white_noise, lags=40, ax=plt.gca())
plt.title("ACF - White Noise")

# 3. Tải và vẽ ACF của chuỗi AirPassengers để so sánh
air_passengers = get_rdataset("AirPassengers").data
ap_series = air_passengers['value']

plt.subplot(1, 2, 2)
plot_acf(ap_series, lags=40, ax=plt.gca())
plt.title("ACF - AirPassengers")

plt.tight_layout()
plt.show()
