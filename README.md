# Time Series Group Project

Deadline chính thức: **14/10/2026**. Deadline nội bộ: **12/10/2026**.

## Mục tiêu

Phân tích chuỗi AirPassengers qua chất lượng dữ liệu, ACF/PACF, white noise, decomposition và trực quan hóa. Mọi kết quả phải tái lập được bằng code và test.

## Phân công

| Người | Module | File chính |
|---|---|---|
| 1 | Dataset & Data Quality | `src/data_quality.py` |
| 2 | ACF/PACF | `src/acf_pacf.py` |
| 3 | White Noise | `src/white_noise.py` |
| 4 | Decomposition | `src/decomposition.py` |
| 5 | Visualization | `src/visualization.py` |
| 6 | Integration, Test, Report | `src/run_all.py` |

## Data contract

File dùng chung: `data/processed/series.csv`

```csv
date,value
1949-01-01,112
```

- `date`: ISO `YYYY-MM-DD`, duy nhất, tăng dần.
- `value`: số, không thiếu trong bản sạch.
- Tần suất: tháng.
- Seasonal period: 12.

## Cài đặt

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Chạy

```powershell
python src/run_all.py
python -m pytest -v
```

## Quy tắc hoàn thành module

Mỗi thành viên phải giao: code, test, hình trong `artifacts/`, section báo cáo trong `reports/sections/`, command và output trong `evidence/`.
