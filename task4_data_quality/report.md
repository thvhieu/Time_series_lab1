# 4. Kiểm tra và xử lý chất lượng dữ liệu

## Input chung

Dataset sử dụng là `data/raw/AirPassengers.csv` gồm 144 dòng và 2 cột `date` và `value`.
- Cột `date` biểu diễn thời gian theo tháng
- Cột `value` biểu diễn số lượng hành khách.

File dữ liệu gốc được giữ nguyên để các task khác trong nhóm có thể sử dụng chung. Các thao tác tạo missing và xử lý dữ liệu được thực hiện trên bản sao, không làm thay đổi file gốc.

## Kiểm tra chất lượng dữ liệu gốc

Dữ liệu được đọc bằng thư viện Pandas.
- Cột `date` được chuyển sang kiểu dữ liệu thời gian bằng `pd.to_datetime()`.
- Cột `value` được chuyển sang kiểu số bằng `pd.to_numeric()`.

Chương trình thực hiện kiểm tra thông tin dữ liệu, các dòng đầu tiên, kiểu dữ liệu, giá trị missing, dòng trùng và ngày trùng.

Kết quả kiểm tra dữ liệu gốc cho thấy:

- Dataset có 144 dòng và 2 cột.
- Không có giá trị missing.
- Không có dòng bị trùng.
- Không có ngày bị trùng.
- Cột `date` có kiểu dữ liệu thời gian và cột `value` có kiểu dữ liệu số sau khi chuyển đổi.

## Tạo dữ liệu thiếu giả lập

Để kiểm tra khả năng xử lý dữ liệu thiếu, chương trình tạo một bản sao từ dữ liệu gốc và thay thế một số giá trị trong cột `value` bằng `NaN`.

Các vị trí được chọn để tạo missing là những dòng có chỉ số `[10, 25, 40, 70, 100, 120]`. Tổng cộng có 6 giá trị được tạo missing nếu các vị trí này đều có dữ liệu hợp lệ ban đầu.

Dữ liệu sau khi tạo missing được lưu tại: `task4_data_quality/output/missing_data.csv`

## Xử lý missing bằng Forward-fill

Forward-fill là phương pháp thay thế giá trị bị thiếu bằng giá trị hợp lệ gần nhất ở phía trước.

Trong chương trình, phương pháp này được thực hiện bằng lệnh: `ffill_df["value"] = ffill_df["value"].ffill()`

Sau khi xử lý, chương trình kiểm tra lại số lượng giá trị missing còn lại. Với dữ liệu mô phỏng hiện tại, các vị trí thiếu đều nằm sau những quan sát có dữ liệu hợp lệ nên Forward-fill có thể thay thế các giá trị này.

Kết quả được lưu tại: `task4_data_quality/output/missing_ffill.csv`

Ưu điểm của Forward-fill là đơn giản và dễ thực hiện. Tuy nhiên, phương pháp này có thể tạo ra các giá trị liên tiếp giống nhau nếu có nhiều vị trí missing liền kề, đồng thời không phản ánh đầy đủ sự thay đổi của chuỗi dữ liệu.

## Xử lý missing bằng Interpolation

Interpolation là phương pháp ước lượng giá trị bị thiếu dựa trên các quan sát có sẵn. Trong bài này, chương trình sử dụng ước tính tuyến tính để tính các giá trị còn thiếu.

Phương pháp được thực hiện bằng lệnh: `interpolation_df["value"] = interpolation_df["value"].interpolate(method="linear"`

Sau khi xử lý, chương trình kiểm tra số lượng giá trị missing còn lại. Với các vị trí missing được tạo trong bài, phương pháp ước tính tuyến tính có thể tính giá trị bị thiếu dựa trên các dữ liệu ở phía trước và phía sau.

Kết quả được lưu tại: `task4_data_quality/output/missing_interpolation.csv`

So với Forward-fill, Interpolation ước tính giá trị bị thiếu dựa trên dữ liệu ở phía trước và phía sau. Phương pháp này giúp dữ liệu thay đổi liên tục hơn. Tuy nhiên, giá trị được điền chỉ là giá trị ước tính không phải số liệu thực tế đã ghi nhận.

## So sánh dữ liệu trước và sau xử lý missing

Chương trình tạo biểu đồ để so sánh dữ liệu gốc, các vị trí được tạo missing, kết quả Forward-fill và kết quả Interpolation.

Biểu đồ được lưu tại: `task4_data_quality/output/missing_comparison.png`

Thông qua biểu đồ, có thể quan sát sự khác biệt giữa hai phương pháp xử lý:

- **Forward-fill:** Điền giá trị bị thiếu bằng giá trị hợp lệ gần nhất phía trước.
- **Interpolation:** Ước lượng giá trị bị thiếu dựa trên các quan sát xung quanh.
- **Dữ liệu gốc:** Được sử dụng làm cơ sở để so sánh và không bị thay đổi trong quá trình xử lý.

Forward-fill phù hợp khi cần giữ lại giá trị gần nhất đã quan sát. Trong khi đó, Interpolation có thể phù hợp hơn khi cần ước lượng các điểm nằm giữa những quan sát đã biết. Việc lựa chọn phương pháp phụ thuộc vào đặc điểm dữ liệu và mục đích phân tích.

## Phát hiện outlier

Outlier là những quan sát có giá trị khác biệt đáng kể so với phần còn lại của dữ liệu. Trong bài này, chương trình sử dụng Z-score để đánh dấu các giá trị có khả năng là outlier, đồng thời tính các thống kê trượt để quan sát sự biến động của chuỗi theo thời gian.

### a. Rolling statistics

Chương trình sử dụng dữ liệu của 12 tháng liên tiếp để tính:

- **Rolling Mean:** Giá trị trung bình của dữ liệu trong 12 tháng.
- **Rolling Variance:** Phương sai cho biết mức độ chênh lệch của các giá trị so với giá trị trung bình.
- **Rolling Standard Deviation:** Độ lệch chuẩn cho biết mức độ dao động của dữ liệu quanh giá trị trung bình.

Các thống kê này giúp quan sát xu hướng và mức độ biến động của dữ liệu theo thời gian.

### b. Z-score

Z-score được tính theo công thức: `Z = (x - mean) / standard deviation`

Trong đó
- `x` là giá trị của một quan sát
- `mean` là giá trị trung bình của toàn bộ chuỗi
- `standard deviation` là độ lệch chuẩn của toàn bộ chuỗi.

Chương trình đánh dấu một quan sát là outlier khi: `abs(Z-score) > 3`

Đây là ngưỡng được sử dụng để xác định các giá trị nằm cách xa trung bình của chuỗi theo độ lệch chuẩn.

Kết quả được lưu tại:

- Dữ liệu kèm các thống kê và kết quả đánh dấu outlier: `task4_data_quality/output/outliers.csv`
- Biểu đồ phát hiện outlier: `task4_data_quality/output/outlier_detection.png`

Cần lưu ý rằng Rolling Mean, Rolling Variance và Rolling Standard Deviation được tính để hỗ trợ quan sát chuỗi còn điều kiện đánh dấu outlier trong chương trình hiện tại dựa trên Z-score toàn cục.

Đối với dữ liệu AirPassengers, số lượng hành khách có xu hướng tăng theo thời gian và có tính mùa vụ. Vì vậy, một số giá trị lớn chưa chắc là dữ liệu sai mà có thể phản ánh đặc điểm tự nhiên của chuỗi. Kết quả phát hiện cần được xem xét trước khi quyết định loại bỏ hoặc điều chỉnh dữ liệu.

## Kết quả và nhận xét

Qua quá trình thực hành, dữ liệu AirPassengers ban đầu được kiểm tra về cấu trúc, kiểu dữ liệu, giá trị missing và dữ liệu trùng. Sau đó, một bản sao dữ liệu được tạo với một số giá trị `NaN` giả lập để kiểm tra khả năng xử lý dữ liệu thiếu.

Hai phương pháp Forward-fill và Interpolation được áp dụng trên bản sao dữ liệu. Forward-fill sử dụng giá trị hợp lệ gần nhất phía trước, trong khi Interpolation ước lượng giá trị thiếu dựa trên các quan sát xung quanh. Kết quả của hai phương pháp được lưu thành các file riêng và so sánh thông qua biểu đồ.

Bên cạnh đó, chương trình tính Rolling Mean, Rolling Variance, Rolling Standard Deviation và sử dụng Z-score để đánh dấu các quan sát có khả năng là outlier. Tuy nhiên, các giá trị được đánh dấu không nhất thiết là dữ liệu sai, đặc biệt đối với chuỗi có xu hướng và tính mùa vụ như AirPassengers.