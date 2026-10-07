# Time Series Group Project

- Deadline chính thức: **14/10/2026**
- Deadline nội bộ: **12/10/2026**
- Dataset chung: `data/processed/series.csv`
- Schema: `date,value`
- Tần suất: tháng; seasonal period: 12

## Cấu trúc đơn giản

```text
Timeseries/
├── data/
│   ├── raw/
│   └── processed/
├── task1_acf_pacf/
│   ├── main.py
│   ├── report.md
│   └── output/
├── task2_white_noise/
│   ├── main.py
│   ├── report.md
│   └── output/
├── task3_decomposition/
│   ├── main.py
│   ├── report.md
│   └── output/
├── task4_data_quality/
│   ├── main.py
│   ├── report.md
│   └── output/
├── task5_visualization/
│   ├── main.py
│   ├── report.md
│   └── output/
├── task6_final_report/
│   ├── run_all.py
│   ├── report.md
│   └── output/
├── .gitignore
├── README.md
└── requirements.txt
```

## Phân công

| Người | Thư mục |
|---|---|
| 1 | `task1_acf_pacf/` |
| 2 | `task2_white_noise/` |
| 3 | `task3_decomposition/` |
| 4 | `task4_data_quality/` |
| 5 | `task5_visualization/` |
| 6 | `task6_final_report/` |

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
