# SaaSeer Frontend-Backend Integration Guide

## Overview

This guide explains how to integrate the React frontend with the FastAPI backend for the SaaSeer Contract Management System.

## Backend API Endpoints

The backend provides the following API endpoints:

### Base URL
- **Development**: `http://localhost:8000/api/v1`
- **Production**: Configure in `.env` file

### Available Endpoints

1. **Health Check**
   - `GET /contracts/health/status`
   - Returns API health status

2. **Contract Management**
   - `GET /contracts?user_email={email}&limit={limit}` - List contracts
   - `POST /contracts` - Create new contract
   - `GET /contracts/{contract_id}?user_email={email}` - Get specific contract
   - `PUT /contracts/{contract_id}?user_email={email}` - Update contract
   - `DELETE /contracts/{contract_id}?user_email={email}` - Delete contract

3. **Expiring Contracts**
   - `GET /contracts/alerts/expiring?user_email={email}` - Get expiring contracts

## Frontend Integration

### API Service Configuration

The frontend uses Axios for API calls with the following configuration:

```javascript
// src/services/api.js
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Data Flow

1. **Authentication**: Simple demo authentication (any email/password)
2. **Contract Operations**: All operations require user email as partition key
3. **Error Handling**: Comprehensive error handling with user-friendly messages
4. **Loading States**: Loading indicators for all async operations

### Contract Data Structure

The frontend expects the following contract data structure:

```javascript
{
  id: "string",
  service_name: "string",
  supplier_name: "string", 
  customer_name: "string",
  contract_start_date: "YYYY/MM/DD",
  contract_end_date: "YYYY/MM/DD",
  contract_details: "string",
  termination_notice_period: "string",
  LinkImage: "string",
  UserEmail: "string",
  created_at: "datetime",
  updated_at: "datetime"
}
```

## Setup Instructions

### 1. Start Backend Server

```bash
cd backend
conda activate py12
python main.py
```

Verify backend is running:
- Visit http://localhost:8000/docs for API documentation
- Visit http://localhost:8000/health for health check

### 2. Start Frontend

```bash
cd frontend
npm install
npm start
```

### 3. Test Integration

1. **Browser Console Test:**
   ```javascript
   // Open browser console and run:
   testSaaSeerAPI()
   ```

2. **Dashboard Status:**
   - Check API connection status in the Dashboard
   - Green indicator = connected
   - Red indicator = connection failed

3. **Manual Testing:**
   - Login with any email/password
   - Try creating a new contract
   - Check if data appears in the contract list

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Backend CORS is configured for `http://localhost:3000`
   - Check if backend is running on correct port

2. **Connection Refused**
   - Ensure backend is running on `http://localhost:8000`
   - Check if conda environment is activated
   - Verify all dependencies are installed

3. **API Errors**
   - Check browser console for detailed error messages
   - Verify API endpoint URLs in `src/services/api.js`
   - Check backend logs for server-side errors

4. **Data Not Loading**
   - Ensure user email is set in localStorage
   - Check if contracts exist for the user email
   - Verify database connection in backend

### Debug Tools

1. **API Test Function:**
   ```javascript
   // In browser console:
   testSaaSeerAPI()
   ```

2. **Network Tab:**
   - Check Network tab in browser DevTools
   - Look for failed API requests
   - Verify request/response data

3. **Backend Logs:**
   - Check backend console for error messages
   - Look for database connection issues
   - Verify request processing

## Environment Configuration

### Frontend (.env)
```env
NODE_ENV=development
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
REACT_APP_APP_NAME=SaaSeer Contract Management
REACT_APP_VERSION=1.0.0
REACT_APP_DEBUG=true
```

### Backend (.env)
```env
COSMOS_ENDPOINT=your_cosmos_endpoint
COSMOS_KEY=your_cosmos_key
COSMOS_DATABASE_NAME=ContractManagement
COSMOS_CONTAINER_NAME=contracts
```

## Production Deployment

1. **Build Frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Configure Production API URL:**
   ```env
   REACT_APP_API_BASE_URL=https://your-api-domain.com/api/v1
   ```

3. **Deploy Backend:**
   - Deploy FastAPI backend to your server
   - Configure CORS for production domain
   - Set up proper environment variables

## API Documentation

For detailed API documentation, visit:
- **Development**: http://localhost:8000/docs
- **Interactive API Explorer**: http://localhost:8000/redoc

## Support

If you encounter issues:

1. Check this integration guide
2. Review browser console errors
3. Check backend server logs
4. Verify all environment variables are set
5. Ensure both servers are running on correct ports
