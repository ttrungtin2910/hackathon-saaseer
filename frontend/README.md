# SaaSeer Contract Management Frontend

Hệ thống quản lý hợp đồng mua sắm được xây dựng với React và Ant Design.

## Tính năng chính

- 🔐 **Đăng nhập/Đăng xuất**: Hệ thống xác thực đơn giản
- 📋 **Quản lý hợp đồng**: Thêm, sửa, xóa, xem chi tiết hợp đồng
- ⚠️ **Cảnh báo hết hạn**: Theo dõi hợp đồng sắp hết hạn
- 🤖 **Báo cáo AI**: Phân tích tự động và khuyến nghị
- 📱 **Giao diện responsive**: Tương thích với mọi thiết bị
- 🌐 **Đa ngôn ngữ**: Hỗ trợ tiếng Việt

## Cấu trúc dự án

```
frontend/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   └── ProtectedRoute.js
│   ├── contexts/
│   │   ├── AuthContext.js
│   │   └── ContractContext.js
│   ├── pages/
│   │   ├── Login.js
│   │   ├── Dashboard.js
│   │   ├── AllContracts.js
│   │   ├── ExpiringContracts.js
│   │   └── Help.js
│   ├── services/
│   │   └── api.js
│   ├── config/
│   │   └── config.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
├── .env
├── .env.example
└── README.md
```

## Installation and Setup

### System Requirements

- Node.js >= 16.0.0
- npm >= 8.0.0
- Backend server running on http://localhost:8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment:
```bash
# Copy configuration template
cp .env.example .env

# Edit .env file for your environment
```

3. Start the application:
```bash
# Development mode
npm start

# Build for production
npm run build
```

### Backend Integration

This frontend is designed to work with the FastAPI backend. Make sure your backend is running:

1. **Start Backend Server:**
```bash
cd backend
conda activate py12
python main.py
```

2. **Verify Backend:**
- Backend should be running on http://localhost:8000
- API docs available at http://localhost:8000/docs
- Health check at http://localhost:8000/health

3. **Test API Connection:**
- Open browser console in the frontend
- Run: `testSaaSeerAPI()`
- Check for connection status in the Dashboard

## Cấu hình

### Biến môi trường

Tạo file `.env` từ `.env.example` và cấu hình:

```env
# Environment Configuration
NODE_ENV=development

# API Configuration
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1

# Application Configuration
REACT_APP_APP_NAME=SaaSeer Contract Management
REACT_APP_VERSION=1.0.0
REACT_APP_DEBUG=true
```

### Kết nối Backend

Ứng dụng frontend kết nối với backend FastAPI thông qua:

- **Base URL**: `http://localhost:8000/api/v1`
- **Proxy**: Cấu hình proxy trong `package.json`
- **CORS**: Backend đã cấu hình CORS cho frontend

## Sử dụng

### Đăng nhập

1. Mở trình duyệt và truy cập `http://localhost:3000`
2. Sử dụng email và mật khẩu bất kỳ để đăng nhập (demo mode)
3. Sau khi đăng nhập thành công, bạn sẽ được chuyển đến trang chủ

### Quản lý Hợp đồng

1. **Xem tất cả hợp đồng**: Truy cập menu "Tất cả hợp đồng"
2. **Thêm hợp đồng mới**: Nhấn nút "Thêm hợp đồng" và điền thông tin
3. **Chỉnh sửa hợp đồng**: Nhấn nút "Sửa" trong bảng danh sách
4. **Xóa hợp đồng**: Nhấn nút "Xóa" và xác nhận
5. **Xem chi tiết**: Nhấn nút "Xem" để xem thông tin đầy đủ

### Cảnh báo Hết hạn

1. Truy cập menu "Hợp đồng sắp hết hạn"
2. Xem danh sách hợp đồng cần chú ý
3. Nhấn "Xem báo cáo AI" để xem phân tích chi tiết

## Công nghệ sử dụng

- **React 18**: Framework chính
- **Ant Design 5**: UI Component Library
- **React Router 6**: Routing
- **Axios**: HTTP Client
- **Context API**: State Management
- **Day.js**: Date manipulation

## API Endpoints

Ứng dụng sử dụng các API endpoints sau:

- `GET /contracts` - Lấy danh sách hợp đồng
- `POST /contracts` - Tạo hợp đồng mới
- `GET /contracts/{id}` - Lấy chi tiết hợp đồng
- `PUT /contracts/{id}` - Cập nhật hợp đồng
- `DELETE /contracts/{id}` - Xóa hợp đồng
- `GET /contracts/alerts/expiring` - Lấy cảnh báo hết hạn

## Phát triển

### Cấu trúc Code

- **Components**: Các component tái sử dụng
- **Pages**: Các trang chính của ứng dụng
- **Contexts**: Quản lý state toàn cục
- **Services**: API calls và business logic
- **Config**: Cấu hình ứng dụng

### Thêm tính năng mới

1. Tạo component trong thư mục `src/components/`
2. Tạo page trong thư mục `src/pages/`
3. Thêm route trong `src/App.js`
4. Cập nhật API service nếu cần
5. Thêm menu item nếu cần

## Troubleshooting

### Lỗi thường gặp

1. **Lỗi kết nối API**: Kiểm tra backend có đang chạy không
2. **Lỗi CORS**: Kiểm tra cấu hình CORS trong backend
3. **Lỗi build**: Xóa `node_modules` và chạy lại `npm install`

### Debug

1. Mở Developer Tools (F12)
2. Kiểm tra Console tab để xem lỗi
3. Kiểm tra Network tab để xem API calls
4. Sử dụng React Developer Tools extension

## Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## License

MIT License - Xem file LICENSE để biết thêm chi tiết.
