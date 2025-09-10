# SaaSeer Contract Management API - Setup Guide

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/ttrungtin2910/hackathon-saaseer.git
cd hackathon-saaseer
```

### 2. Setup Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your actual credentials
# Replace the placeholder values with your Azure Cosmos DB credentials
```

### 3. Install Dependencies
```bash
# Activate conda environment
conda activate py12

# Install Python packages
pip install -r requirements.txt
```

### 4. Start Server
```bash
# Start the FastAPI server
python main.py

# Or use the startup scripts
# Windows:
start_server.bat

# Linux/Mac:
./start_server.sh
```

### 5. Access API
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Base URL**: http://localhost:8000/api/v1/

## 🔧 Configuration

### Environment Variables (.env)
```env
# Azure Cosmos DB Configuration
COSMOS_ENDPOINT=https://your-cosmos-account.documents.azure.com:443/
COSMOS_KEY=your-cosmos-primary-key-here
COSMOS_DATABASE_NAME=ContractManagement
COSMOS_CONTAINER_NAME=contracts

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true
ENVIRONMENT=development
```

### Azure Cosmos DB Setup
1. Create an Azure Cosmos DB account
2. Create a database named "ContractManagement"
3. Create a container named "contracts" with partition key "/UserEmail"
4. Copy the endpoint URL and primary key to your .env file

## 📚 API Usage

### Create Contract
```bash
curl -X POST "http://localhost:8000/api/v1/contracts/" \
  -H "Content-Type: application/json" \
  -d '{
    "contract_data": "{\"id\":\"123\",\"customer_name\":\"Test Company\",\"service_name\":\"Test Service\",\"UserEmail\":\"test@example.com\"}"
  }'
```

### Get Contract
```bash
curl -X GET "http://localhost:8000/api/v1/contracts/123?user_email=test@example.com"
```

### List Contracts
```bash
curl -X GET "http://localhost:8000/api/v1/contracts/?user_email=test@example.com"
```

## 🛡️ Security Notes

- **Never commit .env files** - They contain sensitive credentials
- **Use .env.example** as a template for your configuration
- **Rotate credentials** regularly in production
- **Use environment-specific** configuration files

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the correct conda environment
2. **Database connection**: Verify your Azure Cosmos DB credentials
3. **Port conflicts**: Change PORT in .env if 8000 is occupied
4. **CORS issues**: Check CORS settings in config/settings.py

### Logs
Check the console output for detailed logs with emoji indicators:
- 🚀 Server startup
- 📝 Contract creation
- ✅ Success operations
- ❌ Error messages

## 📖 Documentation

- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)
- **Project README**: README.md
- **Commit Guide**: COMMIT_GUIDE.md

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the SaaSeer hackathon.
