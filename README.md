# SaaSeer Contract Management API

A FastAPI-based backend service for managing contract information with Azure Cosmos DB integration.

## 🚀 Features

- **Contract Management**: Create, read, update, and delete contracts
- **Azure Cosmos DB Integration**: Scalable NoSQL database storage
- **Flexible Data Format**: Supports wrapped JSON data format from frontend
- **Null Values Support**: Handles optional fields gracefully
- **RESTful API**: Clean and intuitive API endpoints
- **Auto Documentation**: Interactive API docs with Swagger UI

## 📋 API Endpoints

### Contract Operations
- `POST /api/v1/contracts/` - Create a new contract
- `GET /api/v1/contracts/{contract_id}` - Get contract by ID
- `PUT /api/v1/contracts/{contract_id}` - Update contract
- `DELETE /api/v1/contracts/{contract_id}` - Delete contract
- `GET /api/v1/contracts/` - List contracts for user

### System
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Azure Cosmos DB account
- Conda (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SaaSeer
   ```

2. **Create conda environment**
   ```bash
   conda create -n py12 python=3.12
   conda activate py12
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure Cosmos DB credentials
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
# Azure Cosmos DB Configuration
COSMOS_ENDPOINT=https://your-cosmos-account.documents.azure.com:443/
COSMOS_KEY=your-cosmos-primary-key
COSMOS_DATABASE_NAME=ContractManagement
COSMOS_CONTAINER_NAME=contracts

# Application Configuration
APP_NAME=SaaSeer Contract Management API
APP_VERSION=1.0.0
DEBUG=False
HOST=0.0.0.0
PORT=8000

# CORS Configuration
CORS_ORIGINS=["*"]
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]
```

## 📊 Data Model

### ContractData
```json
{
  "id": "string (required)",
  "contract_details": "string (optional)",
  "contract_end_date": "string (optional)",
  "contract_start_date": "string (optional)",
  "customer_name": "string (optional)",
  "LinkImage": "string (optional)",
  "service_name": "string (optional)",
  "supplier_name": "string (optional)",
  "termination_notice_period": "string (optional)",
  "UserEmail": "string (optional)",
  "created_at": "datetime (auto-generated)",
  "updated_at": "datetime (auto-generated)"
}
```

## 🔄 Data Format Support

The API supports both direct and wrapped JSON formats:

### Direct Format
```json
{
  "id": "123",
  "customer_name": "Company Name",
  "service_name": "Service Name"
}
```

### Wrapped Format (from frontend)
```json
{
  "contract_data": "{\"id\":\"123\",\"customer_name\":\"Company Name\",\"service_name\":\"Service Name\"}"
}
```

## 🚀 Usage

### Start the server
```bash
# Development mode
python main.py

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example API Call
```bash
curl -X POST "http://localhost:8000/api/v1/contracts/" \
  -H "Content-Type: application/json" \
  -d '{
    "contract_data": "{\"id\":\"123\",\"customer_name\":\"Test Company\",\"service_name\":\"Test Service\"}"
  }'
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 📁 Project Structure

```
SaaSeer/
├── app/
│   ├── __init__.py
│   ├── models.py          # Pydantic models
│   ├── database.py        # Cosmos DB operations
│   └── routes.py          # API endpoints
├── config/
│   ├── __init__.py
│   └── settings.py        # Configuration management
├── tests/
│   ├── __init__.py
│   └── test_contract_api.py
├── scripts/
│   └── run_server.py      # Server startup script
├── docs/
│   └── README.md          # Additional documentation
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes

### Database
- Uses Azure Cosmos DB
- Partition key: `/UserEmail`
- Automatic database and container creation

### Logging
- Structured logging with different levels
- Request/response logging
- Error tracking and debugging

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For support and questions, please contact the development team.

---

**SaaSeer Contract Management API** - Built with FastAPI and Azure Cosmos DB