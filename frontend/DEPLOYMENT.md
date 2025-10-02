# Hướng dẫn Triển khai Frontend

## Triển khai Development

### 1. Cài đặt Dependencies

```bash
cd frontend
npm install
```

### 2. Cấu hình Environment

```bash
# Copy file cấu hình
cp .env.example .env

# Chỉnh sửa .env theo môi trường
```

### 3. Chạy Development Server

```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh

# Hoặc chạy trực tiếp
npm start
```

Ứng dụng sẽ chạy tại: `http://localhost:3000`

## Triển khai Production

### 1. Build ứng dụng

```bash
npm run build
```

### 2. Triển khai với Nginx

Tạo file cấu hình Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Triển khai với Apache

Tạo file `.htaccess`:

```apache
Options -MultiViews
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^ index.html [QSA,L]
```

### 4. Triển khai với Docker

Tạo `Dockerfile`:

```dockerfile
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Tạo `docker-compose.yml`:

```yaml
version: '3.8'
services:
  frontend:
    build: .
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_BASE_URL=http://backend:8000/api/v1

  backend:
    image: your-backend-image
    ports:
      - "8000:8000"
```

## Cấu hình Environment

### Development

```env
NODE_ENV=development
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
REACT_APP_DEBUG=true
```

### Production

```env
NODE_ENV=production
REACT_APP_API_BASE_URL=https://api.yourdomain.com/api/v1
REACT_APP_DEBUG=false
```

## Kiểm tra Triển khai

### 1. Kiểm tra Build

```bash
# Build và kiểm tra
npm run build
npm install -g serve
serve -s build
```

### 2. Kiểm tra API Connection

- Mở Developer Tools
- Kiểm tra Network tab
- Đảm bảo API calls thành công

### 3. Kiểm tra Responsive

- Test trên các kích thước màn hình khác nhau
- Sử dụng Chrome DevTools Device Mode

## Troubleshooting

### Lỗi Build

```bash
# Xóa cache và rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Lỗi API Connection

1. Kiểm tra CORS configuration trong backend
2. Kiểm tra URL API trong .env
3. Kiểm tra network connectivity

### Lỗi Routing

1. Đảm bảo server được cấu hình để serve `index.html` cho tất cả routes
2. Kiểm tra `basename` trong React Router nếu deploy ở subdirectory

## Monitoring

### 1. Log Files

- Nginx: `/var/log/nginx/access.log`
- Apache: `/var/log/apache2/access.log`

### 2. Performance

- Sử dụng Lighthouse để kiểm tra performance
- Monitor bundle size với `npm run build -- --analyze`

### 3. Error Tracking

- Tích hợp Sentry hoặc LogRocket
- Monitor JavaScript errors

## Security

### 1. HTTPS

- Sử dụng SSL certificate
- Redirect HTTP to HTTPS

### 2. Headers

```nginx
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
```

### 3. Environment Variables

- Không commit file .env
- Sử dụng secret management trong production
