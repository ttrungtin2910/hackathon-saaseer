# API Testing Guide - SaaSeer Contract Management

## Overview

This guide explains how to test the API integration between the React frontend and FastAPI backend.

## API Endpoint Details

### List Contracts Endpoint

**URL:** `GET /api/v1/contracts`

**Parameters:**
- `user_email` (required): Email of the user to filter contracts
- `limit` (optional): Maximum number of contracts to return (1-1000, default: 100)

**Example Request:**
```
GET http://localhost:8000/api/v1/contracts?user_email=test@example.com&limit=100
```

**Response Structure:**
```json
{
  "success": true,
  "message": "Contracts retrieved successfully",
  "data": [
    {
      "id": "contract_123",
      "service_name": "Cloud Storage",
      "supplier_name": "AWS",
      "customer_name": "Test Company",
      "contract_start_date": "2024/01/01",
      "contract_end_date": "2024/12/31",
      "contract_details": "Cloud storage service contract",
      "termination_notice_period": "30 days",
      "LinkImage": "https://example.com/image.jpg",
      "UserEmail": "test@example.com",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "count": 1,
  "user_email": "test@example.com"
}
```

## Testing Methods

### 1. Browser Console Testing

Open browser console and run:

```javascript
// Test basic API connection
testSaaSeerAPI()

// Test with specific user email
testContractOperations('your-email@example.com')
```

### 2. Dashboard API Tester

1. Go to Dashboard page
2. Use the "API Tester" component
3. Enter user email and limit
4. Click "Test API" button
5. View detailed response in the interface

### 3. Expiring Contracts Testing

The expiring contracts feature now filters contracts locally instead of using a separate API:
- Contracts are filtered based on `contract_end_date`
- Expired: End date is in the past
- Expiring Soon: End date is within 30 days
- Missing End Date: No end date specified

### 4. Direct API Testing

Use tools like Postman or curl:

```bash
# Test with curl
curl -X GET "http://localhost:8000/api/v1/contracts?user_email=test@example.com&limit=100" \
  -H "Content-Type: application/json"

# Test health check
curl -X GET "http://localhost:8000/api/v1/contracts/health/status"
```

### 4. FastAPI Documentation

Visit the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Troubleshooting

### Common Issues

1. **CORS Errors**
   ```
   Access to XMLHttpRequest at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
   ```
   **Solution**: Ensure backend CORS is configured for frontend origin

2. **Connection Refused**
   ```
   Error: Network Error
   ```
   **Solution**: 
   - Check if backend is running on http://localhost:8000
   - Verify conda environment is activated
   - Check backend logs for errors

3. **404 Not Found**
   ```
   Error: Request failed with status code 404
   ```
   **Solution**: 
   - Verify API endpoint URL is correct
   - Check if backend routes are properly configured
   - Ensure API prefix is correct (/api/v1)

4. **Empty Data Response**
   ```json
   {
     "success": true,
     "data": [],
     "count": 0
   }
   ```
   **Solution**: 
   - Check if contracts exist for the user email
   - Verify database connection
   - Check if user email is correct

### Debug Steps

1. **Check Backend Status**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check API Documentation**
   - Visit http://localhost:8000/docs
   - Test endpoints directly in the interface

3. **Check Frontend Console**
   - Open browser DevTools
   - Look for error messages in Console tab
   - Check Network tab for failed requests

4. **Check Backend Logs**
   - Look at backend console output
   - Check for database connection errors
   - Verify request processing

## Expected Behavior

### Successful API Call

1. **Request**: `GET /api/v1/contracts?user_email=test@example.com&limit=100`
2. **Response**: 200 OK with contract data
3. **Frontend**: Contracts appear in the list
4. **Console**: Success messages in browser console

### Failed API Call

1. **Request**: `GET /api/v1/contracts?user_email=test@example.com&limit=100`
2. **Response**: Error status (400, 500, etc.)
3. **Frontend**: Error message displayed
4. **Console**: Error details logged

## Test Data

### Sample User Emails
- `test@example.com`
- `admin@saaseer.com`
- `user@company.com`

### Sample Contract Data
```json
{
  "service_name": "Cloud Storage",
  "supplier_name": "AWS",
  "customer_name": "Test Company",
  "contract_start_date": "2024/01/01",
  "contract_end_date": "2024/12/31",
  "contract_details": "Cloud storage service contract",
  "termination_notice_period": "30 days",
  "LinkImage": "https://example.com/image.jpg"
}
```

## Performance Testing

### Load Testing
```javascript
// Test with different limits
testContractOperations('test@example.com', 10);   // Small limit
testContractOperations('test@example.com', 100);  // Default limit
testContractOperations('test@example.com', 1000); // Large limit
```

### Error Handling Testing
```javascript
// Test with invalid email
testContractOperations('invalid-email');

// Test with non-existent user
testContractOperations('nonexistent@example.com');
```

## Monitoring

### Frontend Monitoring
- Check browser console for errors
- Monitor network requests in DevTools
- Watch for loading states and error messages

### Backend Monitoring
- Check server logs for errors
- Monitor database connection status
- Watch for performance issues

## Support

If you encounter issues:

1. Check this testing guide
2. Review error messages in console
3. Test API endpoints directly
4. Check backend server status
5. Verify all environment variables are set correctly
