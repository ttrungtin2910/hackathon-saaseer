// Configuration file for different environments
const config = {
  development: {
    API_BASE_URL: 'http://localhost:8000/api/v1',
    APP_NAME: 'SaaSeer Contract Management',
    VERSION: '1.0.0',
    DEBUG: true
  },
  production: {
    API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1',
    APP_NAME: 'SaaSeer Contract Management',
    VERSION: '1.0.0',
    DEBUG: false
  },
  staging: {
    API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1',
    APP_NAME: 'SaaSeer Contract Management',
    VERSION: '1.0.0',
    DEBUG: true
  }
};

// Get current environment
const environment = process.env.NODE_ENV || 'development';

// Export configuration for current environment
export default config[environment];
