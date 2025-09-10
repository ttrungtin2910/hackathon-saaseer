@echo off
echo Cleaning Git history and pushing to GitHub...

echo Step 1: Removing old git repository
rmdir /s /q .git 2>nul

echo Step 2: Initializing fresh git repository
git init

echo Step 3: Configuring git user
git config user.name "SaaSeer Developer"
git config user.email "developer@saaseer.com"

echo Step 4: Adding files
git add .

echo Step 5: Creating clean commit
git commit -m "feat: Initial SaaSeer Contract Management API implementation

- Implement FastAPI backend with Azure Cosmos DB integration
- Support wrapped JSON data format from frontend
- Handle null values for all contract fields
- Add comprehensive error handling and validation
- Include CRUD operations for contract management
- Add proper logging and monitoring
- Support CORS for frontend integration
- Include health check and API documentation endpoints

Features:
- POST /api/v1/contracts/ - Create new contracts
- GET /api/v1/contracts/{id} - Retrieve contract by ID
- PUT /api/v1/contracts/{id} - Update contract
- DELETE /api/v1/contracts/{id} - Delete contract
- GET /api/v1/contracts/ - List contracts by user
- GET /health - Health check endpoint
- GET /docs - API documentation

Technical Stack:
- FastAPI 0.104+
- Azure Cosmos DB SDK
- Pydantic v2 for data validation
- Python 3.12+
- Uvicorn ASGI server"

echo Step 6: Adding remote origin
git remote add origin https://github.com/ttrungtin2910/hackathon-saaseer.git

echo Step 7: Force pushing to GitHub
git push -u origin master --force

echo Done! Repository has been cleaned and pushed to GitHub.
pause
