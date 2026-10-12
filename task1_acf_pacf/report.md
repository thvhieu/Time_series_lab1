# Bài tập 1: Tính và phân tích ACF/PACF

Dataset sử dụng: `AirPassengers.csv` (Số lượng hành khách hàng không theo tháng, 1949 - 1960).

---

## 1. Tải và xem trước dữ liệu (head, info, plot)

### 1.1. Xem trước 5 dòng đầu tiên (`head`) và thông tin cấu trúc (`info`)

* **5 dòng đầu tiên (`df.head()`):**

| date | value |
| :---: | :---: |
| 1949-01-01 | 112 |
| 1949-02-01 | 118 |
| 1949-03-01 | 132 |
| 1949-04-01 | 129 |
| 1949-05-01 | 121 |

* **Thông tin dữ liệu (`df.info()`):**
  * Tổng số quan sát: 144 dòng (144 tháng từ 01/1949 đến 12/1960).
  * Cột thời gian: `date` (kiểu datetime64).
  * Cột giá trị: `value` (kiểu int64, 0 missing).

### 1.2. Biểu đồ dữ liệu chuỗi thời gian (`plot`)

![Biểu đồ chuỗi thời gian AirPassengers](output/airpassengers_time_series.png)

* **Nhận xét nhanh:** Dữ liệu có xu hướng tăng trưởng rõ rệt theo thời gian cùng các đợt dao động mùa vụ lặp lại đều đặn hàng năm với biên độ ngày càng mở rộng.

---

## 2. Tính ACF, PACF đến 40 lags

Tính toán hàm tự tương quan (**ACF**) và hàm tự tương quan từng phần (**PACF**) từ độ trễ 0 đến 40:

![Biểu đồ ACF và PACF đến 40 lags](output/acf_pacf_40lags.png)

* **Bảng giá trị ACF và PACF tại các độ trễ tiêu biểu:**

| Lag | ACF | PACF | Nhận xét |
| :---: | :---: | :---: | :--- |
| **0** | 1.0000 | 1.0000 | Tự tương quan tại độ trễ 0. |
| **1** | 0.9480 | 0.9480 | Tương quan rất cao với tháng liền trước. |
| **2** | 0.8756 | -0.2653 | PACF giảm và đổi chiều sau khi kiểm soát lag 1. |
| **3** | 0.8067 | 0.0555 | PACF tiến gần về dải tin cậy. |
| **12** | **0.7604** | **-0.1580** | **Đỉnh mùa vụ 1 năm (12 tháng)** - ACF nhô cao rõ rệt. |
| **24** | **0.5322** | **0.2778** | **Đỉnh mùa vụ 2 năm (24 tháng)** - ACF tiếp tục tạo đỉnh. |
| **36** | **0.3370** | **0.5239** | **Đỉnh mùa vụ 3 năm (36 tháng)** - ACF lặp lại chu kỳ. |

*(Chi tiết đầy đủ 40 lags được lưu tại [acf_pacf_values.csv](output/acf_pacf_values.csv)).*

---

## 3. Kết luận

### • Chuỗi có tự tương quan mạnh không?
* **Có, tự tương quan rất mạnh.**
* Toàn bộ các hệ số ACF từ lag 1 đến lag 40 đều mang giá trị dương rất cao (từ ~0.95 ở lag 1 và vẫn còn ~0.34 ở lag 40), **vượt xa khỏi dải tin cậy 95%** (vùng màu xanh).
* Điều này chứng tỏ giá trị hiện tại phụ thuộc rất lớn vào các giá trị trong quá khứ.

### • Có xu hướng/mùa vụ thể hiện qua ACF/PACF không?
* **Có cả xu hướng (trend) và mùa vụ (seasonality):**
  * **Xu hướng (Trend):** Biểu đồ ACF giảm dần rất chậm (*slow decay / tính dính*). Đây là dấu hiệu điển hình của chuỗi có xu hướng dài hạn mạnh và không dừng (*non-stationary*).
  * **Mùa vụ (Seasonality):** Biểu đồ ACF dao động tuần hoàn dạng sóng, liên tục xuất hiện các đỉnh nhô cao cục bộ tại các bội số của 12 (**Lag 12, Lag 24, Lag 36**), phản ánh chu kỳ mùa vụ 12 tháng hàng năm.

### • Lag nào quan trọng nhất?
* **Lag 1:** Là lag quan trọng nhất về tương quan ngắn hạn (ACF = 0.948, PACF = 0.948), phản ánh mức độ ảnh hưởng trực tiếp lớn nhất từ thời điểm liền trước.
* **Lag 12 (cùng các bội số 24, 36):** Là các lag quan trọng nhất về tính chu kỳ mùa vụ hàng năm, xác định chu kỳ lặp lại cố định 12 tháng của dữ liệu.
