from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

data = {
    "date": [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
        "2026-01-04",
        "2026-01-05",
        "2026-01-06",
        "2026-01-07",
    ],
    "sales": [100, 105, 103, 110, 108, 115, 120],
}

# Chuyển dictionary thành DataFrame
df = pd.DataFrame(data)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")
df = df.set_index("date")

print("Du lieu:")
print(df)

print("\nMean:", df["sales"].mean())
print("Variance:", df["sales"].var())  #Do mức độ dữ liệu phân tán quanh mean
print("Standard deviation:", df["sales"].std())  # Căn bậc 2 của variance std nhỏ doanh số nằm gần mean , std lớn doanh số biến động mạnh 
# 4 tạo lag 
df["lag_1"] = df["sales"].shift(1) #shift 1 đẩy dữ liệu cột sales xuống 1 dòng 
print("\n du lieu sau khi tao lag 1 :")
print(df)
# ve bieu do 
df["sales"].plot(
    marker ="o",
    title= "Daily Sales",
    figsize=(10,5),
)
plt.xlabel("date")
plt.ylabel("sales")
plt.grid(True)
plt.tight_layout()
plt.show()