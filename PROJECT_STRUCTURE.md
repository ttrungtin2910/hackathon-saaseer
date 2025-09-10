# 📁 SaaSeer Project Structure

```
C:\Users\admin\OneDrive\14_FPT\11-SaaSeer\
├── 📱 app/                          # Main application code
│   ├── __init__.py                  
│   ├── models.py                    # Pydantic data models
│   ├── database.py                  # Azure Cosmos DB operations  
│   └── routes.py                    # FastAPI route definitions
├── ⚙️ config/                       # Configuration management
│   ├── __init__.py
│   └── settings.py                  # Environment settings & validation
├── 🧪 tests/                        # Test files
│   ├── __init__.py
│   └── test_contract_api.py         # API integration tests
├── 🔧 scripts/                      # Utility scripts
│   └── run_server.py                # Enhanced server startup
├── 📚 docs/                         # Documentation
│   └── README.md                    # Detailed project documentation
├── 🚀 main.py                       # FastAPI application entry point
├── 📋 requirements.txt              # Python dependencies
├── 🔐 .env                         # Environment variables (configured)
├── 📝 .env.example                 # Environment template
├── 🪟 start_server.bat             # Windows startup script
├── 🐧 start_server.sh              # Linux/Mac startup script
├── 📖 README.md                    # Main project documentation
└── 📊 PROJECT_STRUCTURE.md         # This structure overview
```

## 🎯 Quick Start Commands

### 1. Start Server (Recommended)
```bash
# Windows
start_server.bat

# Linux/Mac  
chmod +x start_server.sh && ./start_server.sh
```

### 2. Enhanced Python Startup
```bash
conda activate py12
python scripts/run_server.py
```

### 3. Direct Execution
```bash
conda activate py12
pip install -r requirements.txt
python main.py
```

### 4. Test API
```bash
python tests/test_contract_api.py
```

## 🔗 Key URLs
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs  
- **ReDoc**: http://localhost:8000/redoc
- **Health**: http://localhost:8000/health

## 📦 Configuration
- ✅ Azure Cosmos DB credentials configured in `.env`
- ✅ Database: `ContractManagement`
- ✅ Container: `contracts` (auto-created)
- ✅ Partition Key: `/UserEmail`

## 🏗️ Architecture Benefits
- **Separation of Concerns**: App, config, tests in separate modules
- **Dependency Injection**: Settings managed through Pydantic
- **Type Safety**: Full type hints and validation
- **Scalability**: Modular structure for easy feature additions
- **Testing**: Dedicated test directory with integration tests
- **Documentation**: Comprehensive docs and API documentation
- **Environment Management**: Proper .env handling with validation
