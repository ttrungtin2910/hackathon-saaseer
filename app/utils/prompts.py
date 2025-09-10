"""
AI Prompts for LangGraph OpenAI service
Contains template prompts for contract analysis and report generation
"""

# Prompt để trích xuất thông tin từ hợp đồng
CONTRACT_EXTRACTION_PROMPT = """
Bạn là một chuyên gia phân tích hợp đồng. Hãy phân tích nội dung hợp đồng sau và trích xuất các thông tin chính:

Nội dung hợp đồng:
{contract_content}

Hãy trích xuất các thông tin sau (nếu có trong hợp đồng):
1. StartDate (Ngày bắt đầu hợp đồng) - định dạng YYYY-MM-DD
2. EndDate (Ngày kết thúc hợp đồng) - định dạng YYYY-MM-DD  
3. Provider (Nhà cung cấp dịch vụ)
4. Service (Loại dịch vụ)
5. RenewalStatus (Trạng thái gia hạn: "Auto-Renewal", "Manual-Renewal", "No-Renewal", "Unknown")
6. Price (Giá tiền/phí dịch vụ) - chỉ số tiền, không bao gồm ký hiệu tiền tệ
7. Currency (Đơn vị tiền tệ) - ví dụ: USD, EUR, VND, INR

Trả về kết quả dưới dạng JSON với các key tương ứng. Nếu không tìm thấy thông tin nào thì để giá trị null.

Ví dụ:
{
    "StartDate": "2024-01-01",
    "EndDate": "2024-12-31", 
    "Provider": "Microsoft Corporation",
    "Service": "Office 365 Business Premium",
    "RenewalStatus": "Auto-Renewal",
    "Price": "625.00",
    "Currency": "USD"
}
"""

# Prompt để tìm kiếm dịch vụ tương tự
SIMILAR_SERVICE_SEARCH_PROMPT = """
Dựa trên thông tin hợp đồng sau:
- Provider: {provider}
- Service: {service}
- Start Date: {start_date}
- End Date: {end_date}

Và yêu cầu của người dùng: "{user_requirement}"

Hãy tạo các từ khóa tìm kiếm phù hợp để tìm dịch vụ tương tự trên web.
Trả về tối đa 3 cụm từ khóa tìm kiếm, mỗi cụm không quá 5 từ.

Ví dụ:
["cloud storage service pricing", "office productivity tools", "email hosting solutions"]
"""

# Prompt để tạo báo cáo tổng hợp
REPORT_GENERATION_PROMPT = """
Bạn là một chuyên gia tư vấn dịch vụ. Hãy tạo một báo cáo tổng hợp dựa trên:

THÔNG TIN HỢP ĐỒNG HIỆN TẠI:
- Provider: {provider}
- Service: {service}  
- Start Date: {start_date}
- End Date: {end_date}
- Renewal Status: {renewal_status}

YÊU CẦU CỦA NGƯỜI DÙNG:
{user_requirement}

THÔNG TIN DỊCH VỤ TƯƠNG TỰ TÌM ĐƯỢC:
{similar_services}

Hãy tạo một báo cáo chi tiết bao gồm:

1. **TỔNG QUAN HỢP ĐỒNG HIỆN TẠI**
   - Phân tích hợp đồng hiện tại
   - Điểm mạnh và hạn chế

2. **PHÂN TÍCH YÊU CẦU**
   - Hiểu rõ yêu cầu của người dùng
   - Đánh giá mức độ phù hợp với hợp đồng hiện tại

3. **DỊCH VỤ TƯƠNG TỰ TRÊN THỊ TRƯỜNG**
   - So sánh với các dịch vụ tương tự
   - Ưu nhược điểm của từng lựa chọn

4. **KHUYẾN NGHỊ**
   - Đề xuất giải pháp phù hợp nhất
   - Lộ trình thực hiện (nếu cần)

Báo cáo nên có độ dài khoảng 500-800 từ, rõ ràng và dễ hiểu.
"""

# Prompt để xử lý file ảnh/PDF
FILE_CONTENT_EXTRACTION_PROMPT = """
Bạn đang xem nội dung của một file hợp đồng. File này có thể là:
- Ảnh chụp hợp đồng
- File PDF được scan
- File PDF gốc

Hãy đọc và hiểu nội dung, sau đó trích xuất text đầy đủ từ file này.
Tập trung vào các thông tin quan trọng của hợp đồng như:
- Thông tin bên cung cấp dịch vụ
- Thông tin dịch vụ
- Ngày bắt đầu và kết thúc
- Điều khoản gia hạn
- Giá cả và thanh toán

Trả về nội dung text đã được trích xuất một cách có cấu trúc và dễ đọc.
"""

# Prompt để validate dữ liệu trích xuất
DATA_VALIDATION_PROMPT = """
Kiểm tra và xác thực dữ liệu đã trích xuất từ hợp đồng:

Dữ liệu trích xuất:
{extracted_data}

Nội dung gốc:
{original_content}

Hãy:
1. Xác minh tính chính xác của dữ liệu
2. Sửa lỗi định dạng ngày tháng (nếu có)
3. Chuẩn hóa tên nhà cung cấp và dịch vụ
4. Bổ sung thông tin bị thiếu (nếu có thể tìm thấy trong nội dung gốc)

Trả về dữ liệu đã được xác thực và chuẩn hóa dưới dạng JSON.
"""

# Prompt để trích xuất contract data trực tiếp từ file bằng GPT-4 Vision
VISION_CONTRACT_EXTRACTION_PROMPT = """
Bạn là một chuyên gia phân tích hợp đồng. Hãy phân tích file hợp đồng trong hình ảnh và trích xuất các thông tin chính:

Hãy trích xuất các thông tin sau (nếu có trong hợp đồng):
1. StartDate (Ngày bắt đầu hợp đồng) - định dạng YYYY-MM-DD
2. EndDate (Ngày kết thúc hợp đồng) - định dạng YYYY-MM-DD  
3. Provider (Nhà cung cấp dịch vụ)
4. Service (Loại dịch vụ)
5. RenewalStatus (Trạng thái gia hạn: "Auto-Renewal", "Manual-Renewal", "No-Renewal", "Unknown")
6. Price (Giá tiền/phí dịch vụ) - chỉ số tiền, không bao gồm ký hiệu tiền tệ
7. Currency (Đơn vị tiền tệ) - ví dụ: USD, EUR, VND, INR
8. SummaryContract (Tóm lược ngắn gọn nội dung chính của hợp đồng, tối đa 200 từ)

Trả về kết quả dưới dạng JSON với các key tương ứng. Nếu không tìm thấy thông tin nào thì để giá trị null.

Ví dụ:
{
    "StartDate": "2024-01-01",
    "EndDate": "2024-12-31", 
    "Provider": "Microsoft Corporation",
    "Service": "Office 365 Business Premium",
    "RenewalStatus": "Auto-Renewal",
    "Price": "625.00",
    "Currency": "USD",
    "SummaryContract": "Hợp đồng cung cấp dịch vụ Office 365 Business Premium cho doanh nghiệp với 50 licenses, bao gồm email, OneDrive, và các ứng dụng văn phòng. Phí hàng tháng 12.5 USD/user, thanh toán trước 12 tháng. Hợp đồng tự động gia hạn nếu không thông báo hủy trước 30 ngày."
}
"""
