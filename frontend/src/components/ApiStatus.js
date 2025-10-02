import React, { useState, useEffect } from 'react';
import { Alert, Button, Card, Typography, Space } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined, ReloadOutlined } from '@ant-design/icons';
import { contractAPI } from '../services/api';

const { Title, Text } = Typography;

const ApiStatus = () => {
  const [status, setStatus] = useState('checking');
  const [message, setMessage] = useState('Checking API connection...');

  const checkApiStatus = async () => {
    setStatus('checking');
    setMessage('Checking API connection...');
    
    try {
      // Test health check endpoint
      const healthResponse = await contractAPI.healthCheck();
      console.log('Health check response:', healthResponse.data);
      
      if (healthResponse.data.status === 'healthy') {
        setStatus('connected');
        setMessage(`API is running successfully (${healthResponse.data.service || 'contracts'})`);
      } else {
        setStatus('error');
        setMessage('API returned unexpected status');
      }
    } catch (error) {
      setStatus('error');
      console.error('API connection error:', error);
      setMessage(`Connection failed: ${error.message}`);
    }
  };

  useEffect(() => {
    checkApiStatus();
  }, []);

  const getStatusIcon = () => {
    switch (status) {
      case 'connected':
        return <CheckCircleOutlined style={{ color: '#52c41a', fontSize: '24px' }} />;
      case 'error':
        return <CloseCircleOutlined style={{ color: '#ff4d4f', fontSize: '24px' }} />;
      default:
        return <ReloadOutlined spin style={{ color: '#1890ff', fontSize: '24px' }} />;
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'connected':
        return 'success';
      case 'error':
        return 'error';
      default:
        return 'info';
    }
  };

  return (
    <Card style={{ marginBottom: '16px' }}>
      <Space align="center">
        {getStatusIcon()}
        <div>
          <Title level={5} style={{ margin: 0 }}>
            API Connection Status
          </Title>
          <Text type="secondary">{message}</Text>
        </div>
        <Button 
          type="link" 
          icon={<ReloadOutlined />} 
          onClick={checkApiStatus}
          loading={status === 'checking'}
        >
          Refresh
        </Button>
      </Space>
      
      {status === 'error' && (
        <Alert
          message="API Connection Issue"
          description="Please ensure the backend server is running on http://localhost:8000"
          type="error"
          showIcon
          style={{ marginTop: '12px' }}
        />
      )}
    </Card>
  );
};

export default ApiStatus;
