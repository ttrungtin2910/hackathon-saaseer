# Hướng dẫn đánh giá hiệu suất trích xuất thông tin AI

## Tổng quan

Chương trình này đánh giá hiệu suất của mô hình AI trong việc trích xuất thông tin từ hóa đơn và hợp đồng. Mô hình sử dụng GPT-4 Vision để phân tích trực tiếp từ file.

## Các trường thông tin được trích xuất

- **StartDate**: Ngày bắt đầu hợp đồng
- **EndDate**: Ngày kết thúc hợp đồng  
- **Provider**: Nhà cung cấp dịch vụ
- **Service**: Loại dịch vụ
- **RenewalStatus**: Trạng thái gia hạn (Auto-Renewal, Manual-Renewal, No-Renewal, Unknown)
- **SummaryContract**: Tóm tắt nội dung hợp đồng

## Cách sử dụng

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình environment

Đảm bảo file `.env` đã được thiết lập với các API keys cần thiết:
- Azure OpenAI API Key
- Azure OpenAI Endpoint
- Các cấu hình khác theo file `env.example.txt`

### 3. Chạy đánh giá

```bash
python run_evaluation.py
```

hoặc

```bash
python evaluation_script.py
```

## Kết quả đầu ra

### 1. File Excel chi tiết (`contract_extraction_evaluation_results.xlsx`)

**Sheet 1: Tổng quan hiệu suất**
- Tổng số files xử lý
- Tỷ lệ thành công/thất bại
- Thời gian xử lý trung bình, min, max
- Điểm chất lượng dữ liệu trung bình
- Thống kê files theo mức độ hoàn thiện dữ liệu

**Sheet 2: Kết quả chi tiết**
- Kết quả trích xuất từng file
- Thông tin file (tên, kích thước, loại)
- Thời gian xử lý từng file
- Dữ liệu đã trích xuất
- Điểm chất lượng dữ liệu

**Sheet 3: Phân tích dữ liệu**
- Phân tích theo loại file (PDF, PNG)
- Phân tích theo khoảng điểm chất lượng
- Thống kê chi tiết

### 2. File JSON backup (`evaluation_results.json`)
- Lưu trữ toàn bộ dữ liệu dạng JSON
- Tiện cho việc xử lý sau này

### 3. File log (`evaluation_log.txt`)
- Chi tiết quá trình xử lý
- Lỗi và cảnh báo (nếu có)

## Metrics đánh giá

### 1. Tỷ lệ thành công (Success Rate)
- % files được xử lý thành công
- Thước đo chính về độ tin cậy của mô hình

### 2. Thời gian xử lý (Processing Time)
- Thời gian trung bình xử lý mỗi file
- Thời gian min/max để đánh giá performance

### 3. Điểm chất lượng dữ liệu (Data Quality Score)
- Thang điểm 0-100 dựa trên số trường được trích xuất
- StartDate, EndDate: mỗi trường 20 điểm
- Provider, Service: mỗi trường 20 điểm  
- RenewalStatus: 10 điểm
- SummaryContract: 10 điểm

### 4. Phân tích theo loại file
- So sánh hiệu suất giữa PDF và hình ảnh
- Xác định loại file tối ưu

## Troubleshooting

### Lỗi thường gặp

1. **Missing API Keys**: Kiểm tra file `.env` và cấu hình Azure OpenAI
2. **File không đọc được**: Đảm bảo files trong thư mục `data` có định dạng hỗ trợ (.pdf, .png, .jpg, .jpeg)
3. **Memory issues**: Xử lý từng file một để tránh quá tải bộ nhớ
4. **Rate limiting**: Mô hình có thể bị giới hạn rate, script sẽ tự retry

### Tối ưu hiệu suất

1. **Batch processing**: Script đã được tối ưu để xử lý từng file tuần tự
2. **Error handling**: Xử lý lỗi graceful, tiếp tục với file tiếp theo nếu có lỗi
3. **Logging**: Chi tiết log để theo dõi tiến độ và debug

## Mở rộng

### Thêm metrics mới
Chỉnh sửa phương thức `_calculate_data_quality_score()` trong class `ContractExtractionEvaluator`

### Thêm loại file mới  
Cập nhật danh sách `supported_extensions` trong phương thức `get_file_list()`

### Tùy chỉnh format output
Chỉnh sửa các phương thức `_create_*_sheet()` để thay đổi format Excel

## Liên hệ

Nếu có vấn đề hoặc cần hỗ trợ, vui lòng tạo issue hoặc liên hệ team phát triển.
