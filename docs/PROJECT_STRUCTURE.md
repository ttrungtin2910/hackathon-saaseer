# 📁 Cấu trúc dự án SaaSeer

## 🎯 Tổng quan

Dự án đã được tổ chức lại theo cấu trúc enterprise-grade với sự phân tách rõ ràng giữa các thành phần khác nhau.

## 📂 Cấu trúc thư mục

```
SaaSeer/
├── 📁 app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   ├── 📁 config/                   # Application configuration
│   │   ├── __init__.py
│   │   └── settings.py              # Pydantic settings
│   ├── 📁 models/                   # Data models & schemas
│   │   ├── __init__.py
│   │   └── contract.py              # Contract Pydantic models
│   ├── 📁 services/                 # Business logic services
│   │   ├── __init__.py
│   │   ├── azure_blob.py            # Azure Blob Storage service
│   │   ├── cosmosdb.py              # CosmosDB service
│   │   └── langgraph.py             # LangGraph OpenAI service
│   ├── 📁 api/                      # API routes & endpoints
│   │   ├── __init__.py
│   │   └── endpoints.py             # FastAPI route handlers
│   └── 📁 utils/                    # Utility modules
│       ├── __init__.py
│       └── prompts.py               # AI prompt templates
├── 📁 scripts/                      # Startup & utility scripts
│   ├── start.py                     # Development startup script
│   └── start.bat                    # Windows batch script
├── 📁 tests/                        # Test package
│   └── __init__.py
├── 📁 docs/                         # 📚 Documentation
│   ├── README.md                    # Main documentation
│   ├── README_EVALUATION.md         # Evaluation guide
│   └── PROJECT_STRUCTURE.md         # This file
├── 📁 config/                       # ⚙️ Configuration files
│   ├── .env.example                 # Environment variables template
│   └── setup_environment.py         # Environment setup script
├── 📁 evaluation/                   # 🧪 Evaluation & testing
│   ├── demo_evaluation.py           # Demo evaluation script
│   ├── demo_fixed.py                # Fixed demo script
│   ├── evaluation_script.py         # Main evaluation script
│   ├── evaluation_script_fixed.py   # Fixed evaluation script
│   ├── run_evaluation.py            # Evaluation runner
│   └── 📁 logs/                     # Evaluation logs
│       └── evaluation_log.txt       # Evaluation log file
├── 📁 data/                         # 📄 Contract data files
│   └── [100 contract files...]      # PDF, DOCX, PNG files
├── 📁 logs/                         # 📝 Application logs
├── requirements.txt                 # Python dependencies
├── README.md                        # Quick start guide
└── .gitignore                       # Git ignore patterns
```

## 🔄 Thay đổi chính

### ✅ **Đã tổ chức lại:**

1. **Documentation** → `docs/`
   - `README.md` → `docs/README.md`
   - `README_EVALUATION.md` → `docs/README_EVALUATION.md`
   - Tạo `docs/PROJECT_STRUCTURE.md`

2. **Configuration** → `config/`
   - `env.example.txt` → `config/.env.example`
   - `setup_environment.py` → `config/setup_environment.py`

3. **Evaluation Scripts** → `evaluation/`
   - `demo_evaluation.py` → `evaluation/demo_evaluation.py`
   - `demo_fixed.py` → `evaluation/demo_fixed.py`
   - `evaluation_script.py` → `evaluation/evaluation_script.py`
   - `evaluation_script_fixed.py` → `evaluation/evaluation_script_fixed.py`
   - `run_evaluation.py` → `evaluation/run_evaluation.py`
   - `evaluation_log.txt` → `evaluation/logs/evaluation_log.txt`

4. **Logs** → `logs/`
   - Tạo thư mục `logs/` cho application logs

5. **Root README** → Tạo mới
   - `README.md` mới với quick start guide
   - Liên kết đến documentation chi tiết

### 🔧 **Đã cập nhật:**

1. **Import statements** trong các file evaluation
2. **Path references** trong setup scripts
3. **Documentation links** và hướng dẫn

### 🗑️ **Đã dọn dẹp:**

1. **File không cần thiết**: `data.zip`
2. **Tạo `.gitignore`** comprehensive
3. **Tổ chức logs** riêng biệt

## 🚀 **Lợi ích của cấu trúc mới:**

### 📋 **Tổ chức rõ ràng:**
- **Separation of concerns**: Mỗi thư mục có mục đích riêng biệt
- **Easy navigation**: Dễ tìm kiếm và quản lý files
- **Scalable structure**: Dễ mở rộng khi dự án phát triển

### 🔧 **Development friendly:**
- **Clear imports**: Import paths rõ ràng và nhất quán
- **Modular design**: Dễ test và maintain từng module
- **Documentation**: Tài liệu được tổ chức tốt

### 🏢 **Enterprise ready:**
- **Standard structure**: Tuân thủ best practices
- **CI/CD friendly**: Dễ tích hợp với pipeline
- **Team collaboration**: Dễ làm việc nhóm

## 📝 **Hướng dẫn sử dụng:**

### **Development:**
```bash
# Chạy ứng dụng
python scripts/start.py

# Hoặc Windows
scripts\start.bat
```

### **Evaluation:**
```bash
# Demo evaluation
python evaluation/demo_evaluation.py

# Full evaluation
python evaluation/run_evaluation.py
```

### **Configuration:**
```bash
# Setup environment
python config/setup_environment.py

# Copy environment template
cp config/.env.example .env
```

### **Documentation:**
- **Quick Start**: `README.md`
- **Detailed Docs**: `docs/README.md`
- **Evaluation Guide**: `docs/README_EVALUATION.md`
- **Project Structure**: `docs/PROJECT_STRUCTURE.md`

## 🎯 **Next Steps:**

1. **Update CI/CD** pipelines với paths mới
2. **Update deployment** scripts
3. **Add more tests** trong `tests/`
4. **Enhance documentation** trong `docs/`
5. **Setup logging** trong `logs/`

---

*Cấu trúc này được thiết kế để hỗ trợ phát triển dài hạn và dễ dàng maintain.*
