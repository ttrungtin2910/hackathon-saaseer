import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, theme } from 'antd';
import viVN from 'antd/locale/vi_VN';
import { AuthProvider } from './contexts/AuthContext';
import { ContractProvider } from './contexts/ContractContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AllContracts from './pages/AllContracts';
import ExpiringContracts from './pages/ExpiringContracts';
import Help from './pages/Help';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
  const customTheme = {
    algorithm: theme.defaultAlgorithm,
    token: {
      colorPrimary: '#D2B48C',
      colorSuccess: '#52c41a',
      colorWarning: '#faad14',
      colorError: '#ff4d4f',
      colorInfo: '#D2B48C',
      fontFamily: "'Product Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
    },
  };

  return (
    <ConfigProvider locale={viVN} theme={customTheme}>
      <AuthProvider>
        <ContractProvider>
          <Router>
            <div className="App">
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/contracts"
                  element={
                    <ProtectedRoute>
                      <AllContracts />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/expiring"
                  element={
                    <ProtectedRoute>
                      <ExpiringContracts />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/help"
                  element={
                    <ProtectedRoute>
                      <Help />
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </div>
          </Router>
        </ContractProvider>
      </AuthProvider>
    </ConfigProvider>
  );
}

export default App;
