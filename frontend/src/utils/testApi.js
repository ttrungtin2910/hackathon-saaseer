// Utility functions for testing API connection
import { contractAPI } from '../services/api';

export const testApiConnection = async () => {
  try {
    console.log('Testing API connection...');
    const response = await contractAPI.healthCheck();
    console.log('API Health Check Response:', response.data);
    return { success: true, data: response.data };
  } catch (error) {
    console.error('API Connection Test Failed:', error);
    return { 
      success: false, 
      error: error.message,
      details: error.response?.data || null
    };
  }
};

export const testContractOperations = async (userEmail) => {
  try {
    console.log('Testing contract operations...');
    
    // Test getting contracts with detailed logging
    console.log('Calling API: GET /contracts?user_email=' + userEmail + '&limit=100');
    const contractsResponse = await contractAPI.getContracts(userEmail);
    console.log('Get Contracts Response:', contractsResponse.data);
    console.log('Response structure:', {
      success: contractsResponse.data.success,
      message: contractsResponse.data.message,
      data: contractsResponse.data.data,
      count: contractsResponse.data.count,
      user_email: contractsResponse.data.user_email
    });
    
    // Test getting expiring contracts (filtered from all contracts)
    console.log('Filtering expiring contracts from all contracts...');
    const allContracts = contractsResponse.data.data || [];
    const now = new Date();
    const thirtyDaysFromNow = new Date(now.getTime() + (30 * 24 * 60 * 60 * 1000));
    
    const expiringContracts = allContracts.filter(contract => {
      if (!contract.contract_end_date) return false;
      const endDate = new Date(contract.contract_end_date);
      return endDate <= thirtyDaysFromNow && endDate >= now;
    });
    
    console.log(`Found ${expiringContracts.length} expiring contracts:`, expiringContracts);
    
    return { success: true };
  } catch (error) {
    console.error('Contract Operations Test Failed:', error);
    console.error('Error details:', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
      config: {
        url: error.config?.url,
        method: error.config?.method,
        params: error.config?.params
      }
    });
    return { 
      success: false, 
      error: error.message,
      details: error.response?.data || null
    };
  }
};

// Test function that can be called from browser console
window.testSaaSeerAPI = async () => {
  console.log('=== SaaSeer API Test ===');
  
  // Test basic connection
  const connectionTest = await testApiConnection();
  console.log('Connection Test:', connectionTest);
  
  // Test contract operations (requires user email)
  const userEmail = localStorage.getItem('userEmail');
  if (userEmail) {
    const contractTest = await testContractOperations(userEmail);
    console.log('Contract Operations Test:', contractTest);
  } else {
    console.log('No user email found. Please log in first.');
  }
  
  console.log('=== Test Complete ===');
};
