import React, { useState } from 'react';
import { Card, Button, Input, Typography, Space, Alert, Divider, Tag } from 'antd';
import { PlayCircleOutlined, CopyOutlined } from '@ant-design/icons';
import { contractAPI } from '../services/api';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;

const ApiTester = () => {
  const [userEmail, setUserEmail] = useState('test@example.com');
  const [limit, setLimit] = useState('100');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const testListContracts = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      console.log(`Testing API: GET /contracts?user_email=${userEmail}&limit=${limit}`);
      
      const response = await contractAPI.getContracts(userEmail, parseInt(limit));
      
      console.log('API Response:', response);
      
      setResult({
        success: true,
        data: response.data,
        url: response.config?.url,
        method: response.config?.method,
        status: response.status
      });
    } catch (err) {
      console.error('API Test Error:', err);
      setError({
        message: err.message,
        status: err.response?.status,
        data: err.response?.data,
        url: err.config?.url
      });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <Card title="API Tester - List Contracts" style={{ marginBottom: '16px' }}>
      <Space direction="vertical" style={{ width: '100%' }}>
        <div>
          <Text strong>Test Parameters:</Text>
          <Space style={{ marginTop: '8px' }}>
            <Input
              placeholder="User Email"
              value={userEmail}
              onChange={(e) => setUserEmail(e.target.value)}
              style={{ width: '200px' }}
            />
            <Input
              placeholder="Limit"
              value={limit}
              onChange={(e) => setLimit(e.target.value)}
              style={{ width: '100px' }}
            />
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={testListContracts}
              loading={loading}
            >
              Test API
            </Button>
          </Space>
        </div>

        <Divider />

        {result && (
          <div>
            <Title level={5}>✅ API Test Result</Title>
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>
                <Text strong>Request:</Text>
                <Tag color="blue">{result.method} {result.url}</Tag>
              </div>
              <div>
                <Text strong>Status:</Text>
                <Tag color="green">{result.status}</Tag>
              </div>
              <div>
                <Text strong>Response Structure:</Text>
                <div style={{ marginTop: '8px' }}>
                  <Text code>success: {result.data.success ? 'true' : 'false'}</Text><br />
                  <Text code>message: "{result.data.message}"</Text><br />
                  <Text code>count: {result.data.count}</Text><br />
                  <Text code>user_email: "{result.data.user_email}"</Text><br />
                  <Text code>data: Array({result.data.data?.length || 0} items)</Text>
                </div>
                {result.data.data && result.data.data.length > 0 && (
                  <div style={{ marginTop: '12px' }}>
                    <Text strong>Sample Contract Fields:</Text>
                    <div style={{ marginTop: '8px' }}>
                      {Object.keys(result.data.data[0]).map(field => (
                        <Text key={field} code style={{ display: 'block', fontSize: '11px' }}>
                          {field}: {typeof result.data.data[0][field]}
                        </Text>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              <div>
                <Text strong>Full Response:</Text>
                <div style={{ marginTop: '8px', position: 'relative' }}>
                  <Button
                    size="small"
                    icon={<CopyOutlined />}
                    onClick={() => copyToClipboard(JSON.stringify(result.data, null, 2))}
                    style={{ position: 'absolute', top: '8px', right: '8px', zIndex: 1 }}
                  >
                    Copy
                  </Button>
                  <TextArea
                    value={JSON.stringify(result.data, null, 2)}
                    rows={10}
                    readOnly
                    style={{ fontFamily: 'monospace', fontSize: '12px' }}
                  />
                </div>
              </div>
            </Space>
          </div>
        )}

        {error && (
          <div>
            <Title level={5}>❌ API Test Error</Title>
            <Alert
              message="API Call Failed"
              description={
                <div>
                  <Text strong>Error:</Text> {error.message}<br />
                  <Text strong>Status:</Text> {error.status || 'N/A'}<br />
                  <Text strong>URL:</Text> {error.url || 'N/A'}<br />
                  {error.data && (
                    <>
                      <Text strong>Response Data:</Text><br />
                      <Text code>{JSON.stringify(error.data, null, 2)}</Text>
                    </>
                  )}
                </div>
              }
              type="error"
              showIcon
            />
          </div>
        )}
      </Space>
    </Card>
  );
};

export default ApiTester;
