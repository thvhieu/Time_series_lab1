# Time Series Group Project

Dataset dùng chung: `data/raw/AirPassengers.csv` với hai cột `date,value`. Các task đọc trực tiếp file này.

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
| Cột | Kiểu dữ liệu | Mô tả |
|---|---|---|
| date | datetime | Ngày tháng |
| value | Integer | Số lượng hành khách quốc tế |

### 3. Thống kê mô tả

| | Giá trị |
|---|---------|
| Min | **104** (tháng 11/1949) |
| Max | **622** (tháng 7/1960) |
| Trung bình | ~280 |
| Missing | 0  |
| Trùng lặp | 0 |

### 4. Đặc điểm chuỗi
- **Trend:** Tăng trưởng ~4 lần từ 1949 → 1960
- **Seasonality:** Chu kỳ 12 tháng, đỉnh tháng 7–8, đáy tháng 11–12
- **Non-stationary:** Biên độ mùa vụ mở rộng theo thời gian

## Phân công

| Họ tên  | MSSV | Mức độ hoàn thành |Nhiệm vụ|
|---|---|---|--|
| **Trương Hà Vũ Hiệu(L)**| **052206008786**| **100%** | **Task6_final_report**|
| **Phan Ngọc Khoa** | **049206007332** | **100%** | **Task5_visualization**|
| **Trương Lâm Hưng**| **079206003395** | **100%** | **Task1_acf_pacf**|
| **Võ Thị Mỹ Quyên**| **051306013429** | **100%** | **Task2_white_noise**|
| **Lê Ngọc Ánh** |  **051306013023** | **100%** | **Task4_data_quality**|
|**Võ Huy Hoàng**| **089206000185** | **100%** | **Task3_decomposition**|

Cấu trúc lưu trữ:

- `final_report.ipynb`: **Notebook báo cáo tổng hợp toàn bộ đồ án** (kết hợp code chạy trực tiếp, biểu đồ và nhận xét chuyên sâu).
- `script/`: code thực thi từng task riêng lẻ.
- `docs/report/`: báo cáo phương pháp, kết quả, nhận xét dạng markdown.
- `docs/visual/`: biểu đồ hình ảnh (.png).
- `data/process/`: dữ liệu sau xử lý (.csv, .json).

## Cài đặt

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Chạy từng phần

```powershell
python script/task1_acf_pacf.py
python script/task2_white_noise.py
python script/task3_decomposition.py
python script/task4_data_quality.py
python script/task5_visualization.py
```

## Chạy toàn bộ

```powershell
python script/run_all.py
```


