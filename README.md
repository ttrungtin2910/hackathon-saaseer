# SaaSeer - Contract Management System

A comprehensive contract management system with AI-powered contract information extraction capabilities.

## Features

- 📄 **Contract Management**: Create, read, update, delete contracts
- 🤖 **AI-Powered Extraction**: Upload PDF/image contracts and automatically extract key information
- ☁️ **Azure Integration**: Secure file storage with Azure Blob Storage
- 🗄️ **Database Storage**: Azure Cosmos DB for scalable data storage
- 📊 **Dashboard**: Visual contract statistics and expiring contract alerts
- 🔍 **Smart Analysis**: AI-powered contract analysis and recommendations

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Azure Cosmos DB** - NoSQL database
- **Azure Blob Storage** - File storage
- **OpenAI GPT-4 Vision** - AI contract extraction
- **pdf2image** - PDF to image conversion

### Frontend
- **React** - UI framework
- **Ant Design** - UI components
- **Axios** - HTTP client

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 16+
- Azure Storage Account
- Azure Cosmos DB
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SaaSeer
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install Poppler (Required for PDF processing)**
   ```bash
   # For Windows - download from:
   # https://github.com/oschwartz10612/poppler-windows/releases/
   # Extract and add to PATH, or set POPPLER_PATH in .env
   
   # For Linux:
   sudo apt-get install poppler-utils
   
   # For Mac:
   brew install poppler
   ```

4. **Environment Configuration**
   ```bash
   # Copy and configure environment variables
   cp .env.example .env
   # Edit .env with your Azure and OpenAI credentials
   ```

5. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start Backend**
   ```bash
   cd backend
   python main.py
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm start
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Contract Extraction Feature

The system can automatically extract contract information from uploaded files:

### Supported File Types
- PDF files (multi-page support)
- Image files (JPG, PNG, GIF, WEBP)

### Extracted Information
- Supplier name
- Customer name
- Contract start/end dates (normalized to YYYY/MM/DD)
- Termination notice period
- Contract details summary
- Service name

### How It Works
1. Upload contract file through the UI
2. File is stored in Azure Blob Storage
3. PDF is converted to high-resolution images
4. Images are sent to OpenAI GPT-4 Vision API
5. AI extracts structured information
6. Data is saved to Azure Cosmos DB

## API Endpoints

### Contract Management
- `POST /api/v1/contracts` - Create contract
- `GET /api/v1/contracts/{id}` - Get contract by ID
- `PUT /api/v1/contracts/{id}` - Update contract
- `DELETE /api/v1/contracts/{id}` - Delete contract
- `GET /api/v1/contracts` - List contracts by user

### Contract Upload & Extraction
- `POST /api/v1/contracts/upload` - Upload and extract contract information

### Health Check
- `GET /health` - API health status

## Configuration

### Environment Variables

```env
# Azure Cosmos DB
COSMOS_ENDPOINT=https://your-cosmos.documents.azure.com:443/
COSMOS_KEY=your-cosmos-key
COSMOS_DATABASE_NAME=ContractManagement
COSMOS_CONTAINER_NAME=contracts

# Azure Storage
AZURE_SA_URL=https://yourstorage.blob.core.windows.net/
AZURE_SA_KEY=your-storage-key
AZURE_CONTAINER_NAME=contracts

# OpenAI
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4o

# Optional: Poppler path for PDF processing
POPPLER_PATH=C:\path\to\poppler\bin
```

## Project Structure

```
SaaSeer/
├── backend/
│   ├── app/
│   │   ├── database.py          # Cosmos DB operations
│   │   ├── extraction_service.py # AI extraction logic
│   │   ├── models.py            # Data models
│   │   ├── routes.py            # API endpoints
│   │   └── storage_service.py   # Azure Storage operations
│   ├── config/
│   │   └── settings.py          # Configuration
│   ├── main.py                  # FastAPI application
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── contexts/            # React contexts
│   │   ├── pages/               # Page components
│   │   └── services/            # API services
│   └── package.json             # Node dependencies
└── README.md
```

## Development

### Backend Development
```bash
cd backend
python main.py  # Runs with auto-reload
```

### Frontend Development
```bash
cd frontend
npm start  # Runs with hot-reload
```

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

See deployment guides:
- [Backend Deployment](backend/DEPLOYMENT.md)
- [Frontend Deployment](frontend/DEPLOYMENT.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check the API documentation at `/docs`
- Review the deployment guides
- Open an issue on GitHub
