# Contract Management API

Enterprise-grade backend Python API để lưu trữ và truy vấn hợp đồng sử dụng CosmosDB, Azure Blob Storage, và LangGraph OpenAI.

## 🏗️ Cấu trúc dự án

```
SaaSeer/
├── app/                        # Main application package
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py         # Application settings
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   └── contract.py         # Pydantic models for contracts
│   ├── services/               # Business logic services
│   │   ├── __init__.py
│   │   ├── azure_blob.py       # Azure Blob Storage service
│   │   ├── cosmosdb.py         # CosmosDB service
│   │   └── langgraph.py        # LangGraph OpenAI service
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   └── endpoints.py        # FastAPI endpoints
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       └── prompts.py          # AI prompts templates
├── scripts/                    # Startup and utility scripts
│   ├── start.py                # Development startup script
│   └── start.bat               # Windows batch script
├── tests/                      # Test package
│   └── __init__.py
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore patterns
└── .env.example               # Environment variables template
```

## ✨ Tính năng

- 🗄️ **Lưu trữ hợp đồng**: CosmosDB cho metadata, Azure Blob cho files
- 🤖 **AI-powered analysis**: Tự động trích xuất thông tin hợp đồng
- 🔍 **Web search integration**: Tìm dịch vụ tương tự bằng SerpAPI
- 📊 **Intelligent reporting**: Báo cáo tổng hợp thông minh
- 🚀 **RESTful API**: FastAPI với documentation tự động
- 🏢 **Enterprise-ready**: Cấu trúc code chuẩn, scalable

## 🗄️ Database Schema

### CosmosDB Collections

#### ContractInformation
- `id`: Document ID (auto-generated)
- `ContractID`: Contract identifier (UUID)
- `UserName`: User name
- `ContractFilePath`: Azure Blob URL
- `StartDate`: Contract start date
- `EndDate`: Contract end date
- `Provider`: Service provider
- `Service`: Service type
- `RenewalStatus`: Renewal status

#### UserRequirement
- `id`: Document ID (auto-generated)
- `UserRequirementID`: Requirement identifier (UUID)
- `UserRequirementContent`: Requirement content
- `ContractID`: Related contract ID

## 📡 API Endpoints

### 1. List contracts
```http
GET /api/v1/contracts/{username}
```

### 2. Upload contract
```http
POST /api/v1/contracts/upload
Content-Type: multipart/form-data

Body:
- username: string (form data)
- file: file (PDF, JPG, PNG)
```

### 3. Search contracts
```http
POST /api/v1/contracts/search
Content-Type: application/json

{
  "UserName": "string",
  "ContractID": "string", 
  "UserRequirementContent": "string"
}
```

### 4. Get contract requirements
```http
GET /api/v1/contracts/{contract_id}/requirements
```

### 5. Download contract file
```http
GET /api/v1/contracts/{contract_id}/download
```

### 6. Health check
```http
GET /api/v1/health
```

## 🚀 Cài đặt và Chạy

### 1. Clone repository
```bash
git clone <repository-url>
cd SaaSeer
```

### 2. Tạo conda environment
```bash
conda create -n contract python=3.11
conda activate contract
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình Environment Variables

Copy template và cập nhật với thông tin thực:

```bash
# Copy template (Windows)
copy .env.example .env

# Copy template (Linux/Mac)  
cp .env.example .env
```

Cập nhật `.env` với thông tin thực:

```env
# CosmosDB Configuration
COSMOS_ENDPOINT=https://your-cosmos-account.documents.azure.com:443/
COSMOS_KEY=your-cosmos-primary-key
COSMOS_DATABASE_NAME=ContractManagement

# Azure Blob Storage Configuration
AZURE_SA_URL=https://your-storage-account.blob.core.windows.net/
AZURE_SA_KEY=your-storage-account-key
AZURE_CONTAINER_NAME=contracts

# Azure OpenAI Configuration
PROVIDER_NAME=azure_openai
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
OPENAI_API_VERSION=2024-12-01-preview
OPENAI_MODEL_NAME=gpt-4o-mini
OPENAI_TIME_OUT=10
AZ_OPENAI_TEMP=0.3
AZ_MAX_TOKEN=1000

# Legacy OpenAI Configuration (fallback)
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=True

# SerpAPI Configuration
SERPAPI_API_KEY=your-serpapi-key
```

### 5. Chạy ứng dụng

#### Development với conda
```bash
conda activate contract
python scripts/start.py
```

#### Windows batch script
```bash
scripts\start.bat
```

#### Production với uvicorn
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 6. Truy cập API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 🔄 Quy trình hoạt động

### Upload hợp đồng:
1. User upload file → Azure Blob Storage
2. LangGraph OpenAI phân tích nội dung file
3. Trích xuất thông tin hợp đồng tự động
4. Lưu metadata vào CosmosDB

### Search & Report:
1. Lưu yêu cầu user vào UserRequirement table
2. SerpAPI tìm kiếm dịch vụ tương tự trên web
3. LangGraph tạo báo cáo tổng hợp thông minh
4. Trả về kết quả chi tiết

## 🏢 Enterprise Features

- **Modular Architecture**: Tách biệt concerns, dễ maintain
- **Service Layer**: Business logic được tổ chức trong services
- **Type Safety**: Pydantic models cho data validation
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging across all modules
- **Testing Ready**: Test package structure prepared
- **Docker Ready**: Easy containerization
- **CI/CD Friendly**: Standard Python project structure

## 🧪 Development

### Project Structure Benefits
- **Separation of Concerns**: API, models, services tách biệt
- **Import Management**: Clean imports với __init__.py
- **Scalability**: Dễ thêm features mới
- **Testing**: Test structure sẵn sàng
- **Deployment**: Production-ready structure

### Adding New Features
1. **Models**: Add to `app/models/`
2. **Services**: Add to `app/services/`
3. **APIs**: Add to `app/api/`
4. **Utils**: Add to `app/utils/`

## 📋 Requirements

- **Python**: 3.11+
- **Azure**: CosmosDB + Blob Storage accounts
- **OpenAI**: API key for GPT-4
- **SerpAPI**: API key for web search
- **Conda**: For environment management

## 🎯 Production Deployment

1. **Environment**: Cập nhật production credentials
2. **Security**: Configure CORS, authentication
3. **Monitoring**: Add application monitoring
4. **Scaling**: Consider container orchestration
5. **Backup**: Setup database backup strategies

## 📞 Support

- **Documentation**: Check `/docs` endpoint
- **Health Check**: Monitor `/api/v1/health`
- **Logs**: Application logs for debugging
- **Structure**: Follow established patterns for new features