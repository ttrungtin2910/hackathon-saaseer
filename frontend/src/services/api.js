import axios from 'axios';
import config from '../config/config';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: config.API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      localStorage.removeItem('userEmail');
      window.location.href = '/login';
    } else if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
      // Handle connection errors
      console.error('Backend connection failed. Please ensure the server is running on http://localhost:8000');
    }
    return Promise.reject(error);
  }
);

// Contract API endpoints
export const contractAPI = {
  // Get all contracts for a user
  getContracts: (userEmail, limit = 100) => 
    api.get(`/contracts?user_email=${userEmail}&limit=${limit}`),

  // Get a specific contract
  getContract: (contractId, userEmail) => 
    api.get(`/contracts/${contractId}?user_email=${userEmail}`),

  // Create a new contract
  createContract: (contractData) => 
    api.post('/contracts', contractData),

  // Update a contract
  updateContract: (contractId, userEmail, updateData) => 
    api.put(`/contracts/${contractId}?user_email=${userEmail}`, updateData),

  // Delete a contract
  deleteContract: (contractId, userEmail) => 
    api.delete(`/contracts/${contractId}?user_email=${userEmail}`),

  // Health check
  healthCheck: () => 
    api.get('/contracts/health/status'),
};

// Auth API endpoints
export const authAPI = {
  // Simple login (for demo purposes)
  login: (email, password) => {
    // In a real app, this would call your auth endpoint
    return new Promise((resolve) => {
      setTimeout(() => {
        if (email && password) {
          localStorage.setItem('authToken', 'demo-token');
          localStorage.setItem('userEmail', email);
          resolve({ success: true, data: { email } });
        } else {
          resolve({ success: false, message: 'Invalid credentials' });
        }
      }, 1000);
    });
  },

  // Logout
  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userEmail');
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('authToken');
  },

  // Get current user email
  getCurrentUser: () => {
    return localStorage.getItem('userEmail');
  },
};

export default api;
