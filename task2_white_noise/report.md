# 3. Kiểm tra White Noise

## Phương pháp

Sinh dữ liệu White Noise bằng NumPy với 1000 điểm dữ liệu (phân phối chuẩn, trung bình bằng 0, độ lệch chuẩn bằng 1).

Sử dụng hàm plot_acf từ thư viện statsmodels để vẽ biểu đồ hàm tự tương quan (ACF) đến 40 lag.

Tải chuỗi dữ liệu thực tế AirPassengers từ statsmodels và vẽ biểu đồ ACF tương tự để tiến hành đối chiếu, so sánh.

## Kết quả

Biểu đồ ACF của White Noise: Các hệ số tự tương quan ở các lag lớn hơn 0 dao động ngẫu nhiên xung quanh 0 và nằm trọn bên trong dải tin cậy 95%.

Biểu đồ ACF của AirPassengers: Các hệ số tự tương quan có giá trị rất cao, giảm dần rất chậm qua các lag và xuất hiện các đỉnh sóng lặp lại theo chu kỳ mùa vụ, vượt ra ngoài ngưỡng tin cậy 95%.

## Nhận xét

Về tự tương quan: Chuỗi White noise thể hiện tính độc lập hoàn toàn theo thời gian (không có tự tương quan), trong khi AirPassengers có mức độ tự tương quan cực kỳ cao và bền vững qua các lag.

Về xu hướng và chu kỳ: White noise mang tính ngẫu nhiên thuần túy, không chứa xu hướng hay mùa vụ; ngược lại, AirPassengers phản ánh rõ rệt xu hướng tăng trưởng dài hạn và tính mùa vụ theo năm.

Về khả năng dự báo: Chuỗi White noise không thể dự báo dựa vào dữ liệu quá khứ do bản chất ngẫu nhiên hoàn toàn, còn chuỗi AirPassengers rất thích hợp và tiềm năng để xây dựng các mô hình dự báo chuỗi thời gian chuyên sâu như ARIMA hoặc SARIMA.
