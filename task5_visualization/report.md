# 5. Trực quan hóa dữ liệu chuỗi thời gian

## Phương pháp

Dữ liệu: **AirPassengers** (01/1949 – 12/1960), 144 quan sát tháng, đơn vị nghìn hành khách.

Bốn biểu đồ được thực hiện:

| # | Biểu đồ | File |
|---|---|---|
| 1 | Line chart toàn bộ chuỗi | `01_line_chart.png` |
| 2 | Rolling mean & rolling std (window=12) | `02_rolling_stats.png` |
| 3 | Seasonal plot theo tháng | `03_seasonal_plot.png` |
| 4 | Heatmap seasonality (month × year) | `04_heatmap.png` |

## Kết quả

**Biểu đồ 1 – Line chart:** Chuỗi tăng liên tục từ 112 (01/1949) lên 622 nghìn (07/1960), xuất hiện dao động lên-xuống đều đặn hàng năm.

**Biểu đồ 2 – Rolling stats:** Rolling mean tăng đều qua các năm; rolling std cũng tăng theo, từ ~15 (1950) lên ~65 (1960), cho thấy chuỗi **không dừng** và phương sai không đồng nhất.

**Biểu đồ 3 – Seasonal plot:** Mỗi tháng cho thấy xu hướng tăng rõ ràng. Tháng 7–8 luôn cao nhất, tháng 11–12 thấp nhất; mẫu mùa vụ **lặp lại nhất quán** qua 12 năm.

**Biểu đồ 4 – Heatmap:** Vùng màu đậm tập trung ở các hàng tháng 7–8 (mùa hè) và ngả sang màu nhạt ở tháng 11–2. Màu sắc đậm dần từ trái sang phải xác nhận xu hướng tăng theo năm.

## Kết luận

1. **Xu hướng chung:** Số hành khách tăng mạnh (~5,5× trong 12 năm), phản ánh sự bùng nổ của hàng không dân dụng thập niên 1950.

2. **Mùa vụ nổi bật:** Chu kỳ 12 tháng rõ rệt – đỉnh vào tháng 7–8 (hè), đáy vào tháng 11–12 (đông). Biên độ mùa vụ tăng dần theo thời gian → mô hình mùa vụ **multiplicative**.

3. **Bất thường:** Không có điểm ngoại lệ đột biến bất thường. Năm 1958 tăng trưởng chậm lại nhẹ, phù hợp bối cảnh suy thoái kinh tế Mỹ 1957–1958, không phải lỗi dữ liệu.
