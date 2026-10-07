# Quy trình đóng góp

1. Cập nhật `main`: `git switch main; git pull origin main`.
2. Tạo branch riêng: `git switch -c task/<module>`.
3. Chỉ sửa module, test, artifact và section báo cáo được phân công.
4. Chạy script và `python -m pytest -v` trước khi push.
5. Push branch và mở Pull Request vào `main`.
6. Không push trực tiếp lên `main`; người tích hợp review và merge.

## Tên branch

- `task/data-quality`
- `task/acf-pacf`
- `task/white-noise`
- `task/decomposition`
- `task/visualization`
- `task/integration`
