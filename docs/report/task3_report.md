# Báo cáo phân rã chuỗi thời gian AirPassengers

## 1. Phương pháp

Sử dụng **classical multiplicative decomposition** với chu kỳ mùa vụ `period = 12` tháng. Mô hình:

\[Y_t = T_t \times S_t \times R_t\]

Dữ liệu có **144 quan sát tháng**, từ **1949-01** đến **1960-12**. Biểu đồ phân rã lưu tại `output/decomposition_plot.png`.

## 2. Kết quả

### 2.1. Xu hướng (Trend)
- Trend đầu kỳ: **118.59**; cuối kỳ: **503.80**.
- Thay đổi tổng cộng: **324.83%** (CAGR: **12.91%/năm**).
- Độ dốc tuyến tính: **2.6726 đơn vị/tháng** (R² = **0.9861**).
- Độ mạnh xu hướng: **0.9933**.
- Kết luận: xu hướng tổng quát **tăng**.

### 2.2. Mùa vụ (Seasonal)
- Tháng đỉnh mùa vụ: **Jul** (index = **1.2294**).
- Tháng đáy mùa vụ: **Nov** (index = **0.7979**).
- Chênh lệch đỉnh/đáy: **54.09%**.
- Độ mạnh mùa vụ: **0.9293**.

### 2.3. Phần dư (Residual) và white noise
- Trung bình của `Residual - 1`: **0.00039**.
- Độ lệch chuẩn của `Residual - 1`: **0.03537**.
- ACF tại độ trễ 1: **0.4594**.
- p-value Ljung–Box: **{"12": 2.2166758280143447e-18, "24": 1.0154630722249876e-27}**.
- Kiểm định Ljung–Box tại độ trễ 12 có p-value ≤ 0,05; bác bỏ giả thuyết không có tự tương quan. Residual chưa thể xem là white noise.

## 3. Nhận xét
1. **Xu hướng:** Tăng rõ nét theo thời gian.
2. **Mùa vụ:** Mùa vụ mạnh với đỉnh vào Jul và đáy vào Nov.
3. **Residual:** còn tồn tại tự tương quan tại lag 12.

## Danh mục tệp đầu ra
- `report.md`: Báo cáo phương pháp, kết quả và nhận xét.
- `output/decomposition_results.csv`: Dữ liệu phân rã chi tiết.
- `output/monthly_seasonal_indices.csv`: Chỉ số mùa vụ theo từng tháng.
- `output/decomposition_plot.png`: Biểu đồ 4 thành phần.
- `output/residual_diagnostics.png`: Đồ thị phân tích phần dư và ACF.
- `output/seasonal_pattern.png`: Biểu đồ cột chỉ số mùa vụ.
- `output/analysis_summary.json`: Tóm tắt các chỉ số thống kê.
