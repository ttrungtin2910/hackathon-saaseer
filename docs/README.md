# SaaSeer Contract Management API

A FastAPI backend application for managing contract information with Azure Cosmos DB storage.

## Features

- ✅ Create, read, update, and delete contracts
- ✅ Store contract data in Azure Cosmos DB
- ✅ RESTful API with automatic documentation
- ✅ Pydantic data validation
- ✅ CORS support for web applications
- ✅ Comprehensive error handling
- ✅ Health check endpoints
- ✅ Async/await support for high performance
- ✅ Proper project structure and configuration management

## Project Structure

```
├── app/                     # Main application code
│   ├── __init__.py         
│   ├── models.py           # Pydantic data models
│   ├── database.py         # Azure Cosmos DB operations
│   └── routes.py           # API route definitions
├── config/                 # Configuration management
│   ├── __init__.py
│   └── settings.py         # Settings and environment variables
├── tests/                  # Test files
│   ├── __init__.py
│   └── test_contract_api.py # API integration tests
├── scripts/                # Utility scripts
│   └── run_server.py       # Enhanced server startup script
├── docs/                   # Documentation
│   └── README.md           # This file
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (configured)
├── .env.example           # Environment variables template
├── start_server.bat       # Windows startup script
└── start_server.sh        # Linux/Mac startup script
```

## Prerequisites

- Python 3.8+
- Azure Cosmos DB account
- pip or conda package manager
- Conda environment 'py12' (recommended)

## Quick Start

### 1. Installation

```bash
# Clone or download the project files
# Navigate to the project directory

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

The `.env` file has been configured with your Azure Cosmos DB credentials:
- Database: `ContractManagement`
- Endpoint: `https://fjp-bachan-cosmosdb-dev.documents.azure.com:443/`

### 3. Run the Application

#### Option 1: Using startup scripts (recommended)
```bash
# On Windows
start_server.bat

# On Linux/Mac
chmod +x start_server.sh
./start_server.sh
```

#### Option 2: Using enhanced Python script
```bash
# Activate conda environment first
conda activate py12

# Run enhanced startup script
python scripts/run_server.py
```

#### Option 3: Direct execution
```bash
# Activate conda environment
conda activate py12

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Contract Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/contracts/` | Create a new contract |
| POST | `/api/v1/contracts/quick-create` | Quick create (accepts raw format) |
| GET | `/api/v1/contracts/{contract_id}` | Get contract by ID |
| PUT | `/api/v1/contracts/{contract_id}` | Update contract |
| DELETE | `/api/v1/contracts/{contract_id}` | Delete contract |
| GET | `/api/v1/contracts/` | List user's contracts |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | General health check |
| GET | `/api/v1/contracts/health/status` | Contract service health |

## Usage Examples

### Create a Contract

```bash
curl -X POST "http://localhost:8000/api/v1/contracts/quick-create" \
     -H "Content-Type: application/json" \
     -d '{
       "contract_details": "所在地: 東京都港区三田三丁目５番１９号、面積: 5.19㎡(1.57坪)、月額金123,550円、支払期日: 翌月分を毎月20日までに支払",
       "contract_end_date": "2028/06/30",
       "contract_start_date": "2025/09/01",
       "customer_name": "ＦＰＴジャパンホールディングス株式会社",
       "id": "c5d847a2-6fde-41d4-aaf3-b676ad3f8151",
       "LinkImage": "https://fptsoftware362-my.sharepoint.com/:b:/g/personal/tintt33_fpt_com/Efm3DWFRE89GqTJAnB7OV1UBzMiHtO3c_DQXlMbw5y7Udw",
       "service_name": "防災備蓄倉庫",
       "supplier_name": "住友不動産株式会社",
       "termination_notice_period": "契約期間満了の1年前から6ヶ月前まで",
       "UserEmail": "tintt33@fpt.com"
     }'
```

### Get a Contract

```bash
curl -X GET "http://localhost:8000/api/v1/contracts/c5d847a2-6fde-41d4-aaf3-b676ad3f8151?user_email=tintt33@fpt.com"
```

### Test the API

```bash
# Run the integration test
python tests/test_contract_api.py
```

## Data Model

### Contract Data Structure

```json
{
  "id": "string (UUID)",
  "contract_details": "string (Japanese text with location, area, amount, payment info)",
  "contract_end_date": "string (YYYY/MM/DD format)",
  "contract_start_date": "string (YYYY/MM/DD format)", 
  "customer_name": "string (Company name in Japanese)",
  "LinkImage": "string (URL to contract document)",
  "service_name": "string (Service name in Japanese)",
  "supplier_name": "string (Supplier company name in Japanese)",
  "termination_notice_period": "string (Notice period in Japanese)",
  "UserEmail": "string (Email address - used as partition key)",
  "created_at": "datetime (Auto-generated)",
  "updated_at": "datetime (Auto-updated)"
}
```

## Azure Cosmos DB Configuration

The application is configured to use your Azure Cosmos DB:
- **Endpoint**: `https://fjp-bachan-cosmosdb-dev.documents.azure.com:443/`
- **Database**: `ContractManagement`
- **Container**: `contracts`
- **Partition Key**: `/UserEmail`

The application will automatically create the database and container if they don't exist.

## Configuration Management

Configuration is handled through the `config/settings.py` module using Pydantic settings:

- Environment variables are loaded from `.env` file
- Settings are validated and type-checked
- Default values are provided for optional settings
- Settings can be dependency-injected in FastAPI routes

## Development

### Adding New Features

1. Define new models in `app/models.py`
2. Add database operations in `app/database.py`
3. Create new routes in `app/routes.py`
4. Include routes in `main.py`
5. Add tests in `tests/`

### Running Tests

```bash
# Run API integration tests
python tests/test_contract_api.py

# For unit tests (add pytest tests in tests/ directory)
pytest tests/
```

## Production Deployment

1. Set `DEBUG=false` in environment variables
2. Configure proper CORS origins in settings
3. Use a production WSGI server like Gunicorn
4. Set up proper logging and monitoring
5. Configure Azure Cosmos DB with appropriate throughput

```bash
# Production run example
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `SaaSeer Contract Management API` |
| `APP_VERSION` | Application version | `1.0.0` |
| `DEBUG` | Debug mode | `true` |
| `ENVIRONMENT` | Environment | `development` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `COSMOS_ENDPOINT` | Azure Cosmos DB endpoint URL | Required |
| `COSMOS_KEY` | Azure Cosmos DB primary key | Required |
| `COSMOS_DATABASE_NAME` | Database name | `ContractManagement` |
| `COSMOS_CONTAINER_NAME` | Container name | `contracts` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Troubleshooting

### Common Issues

1. **Cosmos DB Connection Failed**
   - Check endpoint URL and primary key in `.env`
   - Verify network connectivity
   - Ensure Cosmos DB account is active

2. **Module Import Errors**
   - Ensure you're in the project root directory
   - Activate the correct conda environment: `conda activate py12`
   - Install dependencies: `pip install -r requirements.txt`

3. **Permission Denied**
   - Verify Cosmos DB key has read/write permissions
   - Check container permissions

4. **Validation Errors**
   - Ensure all required fields are provided
   - Check data types match the model definition

### Logging

The application logs important events and errors. Check the console output or configure file logging for production use.

## License

MIT License - see LICENSE file for details.

## Support

For support, contact FPT Software team or create an issue in the project repository.
