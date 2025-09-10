# Contract Management API

Enterprise-grade backend Python API để lưu trữ và truy vấn hợp đồng sử dụng CosmosDB, Azure Blob Storage, và LangGraph OpenAI.

## 🚀 Quick Start

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Cấu hình Environment
```bash
# Copy template
cp config/.env.example .env

# Cập nhật .env với thông tin thực
```

### 3. Chạy ứng dụng
```bash
# Development
python scripts/start.py

# Hoặc Windows
scripts\start.bat

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Truy cập API
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## 📁 Project Structure

```
SaaSeer/
├── app/                    # Main application
│   ├── main.py            # FastAPI entry point
│   ├── config/            # Configuration
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   ├── api/               # API routes
│   └── utils/             # Utilities
├── scripts/               # Startup scripts
├── tests/                 # Test package
├── docs/                  # Documentation
├── config/                # Configuration files
├── evaluation/            # Evaluation scripts
├── data/                  # Contract files
├── logs/                  # Application logs
└── requirements.txt       # Dependencies
```

## 📚 Documentation

- **[Main Documentation](docs/README.md)** - Chi tiết về API và cấu hình
- **[Evaluation Guide](docs/README_EVALUATION.md)** - Hướng dẫn đánh giá hệ thống

## 🔧 Configuration

Tất cả file cấu hình được tổ chức trong thư mục `config/`:
- `.env.example` - Template cho environment variables
- `setup_environment.py` - Script setup môi trường

## 🧪 Evaluation

Scripts đánh giá hệ thống được tổ chức trong thư mục `evaluation/`:
- `demo_evaluation.py` - Demo đánh giá
- `evaluation_script.py` - Script đánh giá chính
- `run_evaluation.py` - Chạy đánh giá
- `logs/` - Logs đánh giá

## 📋 Requirements

- **Python**: 3.11+
- **Azure**: CosmosDB + Blob Storage accounts
- **OpenAI**: API key for GPT-4
- **SerpAPI**: API key for web search

## 🎯 Features

- 🗄️ **Contract Storage**: CosmosDB + Azure Blob
- 🤖 **AI Analysis**: LangGraph OpenAI integration
- 🔍 **Web Search**: SerpAPI integration
- 📊 **Smart Reporting**: Intelligent contract analysis
- 🚀 **RESTful API**: FastAPI with auto-documentation
- 🏢 **Enterprise Ready**: Scalable architecture

## 📞 Support

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Logs**: Check `logs/` directory
