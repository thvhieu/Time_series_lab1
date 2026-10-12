
## Mô tả Dataset — AirPassengers

### 1. Tổng quan

| Thuộc tính | Giá trị |
|------------|---------|
| Tên dataset | AirPassengers |
| Nguồn | Box & Jenkins (1976) |
| Số dòng | **144** |
| Khoảng thời gian | **01/1949 – 12/1960** |
| Tần suất | Hàng tháng |
| Đơn vị | Nghìn hành khách |

### 2. Mô tả cột 
|Cột | Kiểu dữ liệu | Mô tả |
|--|--|--|
| date | datetime | Ngày tháng |
| value | Integer | Số lượng hành khách quốc tế |

### 3. Thống kê mô tả

| | Giá trị |
|--|---------|
| Min | **104** (tháng 11/1949) |
| Max | **622** (tháng 7/1960) |
| Trung bình | ~280 |
| Missing | 0  |
| Trùng lặp | 0 |

### 4. Đặc điểm chuỗi
- **Trend:** Tăng trưởng ~4 lần từ 1949 → 1960
- **Seasonality:** Chu kỳ 12 tháng, đỉnh tháng 7–8, đáy tháng 11–12
- **Non-stationary:** Biên độ mùa vụ mở rộng theo thời gian


---

### 5. Kết luận: Dữ liệu có phù hợp để dự báo không?

**✅ Phù hợp** — AirPassengers là một trong những dataset chuẩn mực để thực hành dự báo chuỗi thời gian, với các lý do sau:

| Tiêu chí | Đánh giá |
|----------|----------|
| Dữ liệu đầy đủ, không bị thiếu | ✅ Tốt |
| Có cấu trúc rõ ràng (trend + seasonality) | ✅ Tốt |
| Đủ độ dài (144 quan sát = 12 năm) | ✅ Tốt |
| Tần suất phù hợp (monthly) | ✅ Tốt |
| Chuỗi không dừng (cần xử lý trước) | ⚠️ Cần differencing/log-transform |

**Khuyến nghị tiền xử lý trước khi dự báo:**
- Áp dụng **log-transform** để ổn định phương sai (biên độ mùa vụ tăng dần)
- Áp dụng **differencing bậc 1** để loại bỏ trend
- Áp dụng **seasonal differencing (lag=12)** để loại bỏ mùa vụ

**Mô hình phù hợp:** SARIMA(p,d,q)(P,D,Q)[12] — mô hình ARIMA có thành phần mùa vụ theo chu kỳ 12 tháng.
