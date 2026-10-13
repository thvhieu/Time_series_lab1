# Time Series Group Project

Dataset dùng chung: `data/raw/AirPassengers.csv` với hai cột `date,value`. Các task đọc trực tiếp file này.

## Phân công

| Họ tên  | MSSV | Mức độ hoàn thành |Nhiệm vụ|
|---|---|---|--|
| **Trương Hà Vũ Hiệu(L)**| **052206008786**| **100%** | **Task6_final_report**|
| **Phan Ngọc Khoa** | **049206007332** | **100%** | **Task5_visualization**|
| **Trương Lâm Hưng**| **079206003395** | **100%** | **Task1_acf_pacf**|
| **Võ Thị Mỹ Quyên**| **051306013429** | **100%** | **Task2_white_noise**|
| **Lê Ngọc Ánh** |  **051306013023** | **100%** | **Task4_data_quality**|
|**Võ Huy Hoàng**| **089206000185** | **100%** | **Task3_decomposition**|

Mỗi người chỉ sửa thư mục của mình. Trong đó:

- `main.py`: code.
- `report.md`: phương pháp, kết quả, nhận xét.
- `output/`: biểu đồ và file kết quả.

## Cài đặt

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Chạy từng phần

```powershell
python task1_acf_pacf/main.py
python task2_white_noise/main.py
python task3_decomposition/main.py
python task4_data_quality/main.py
python task5_visualization/main.py
```

## Chạy toàn bộ

```powershell
python task6_final_report/run_all.py
```


