import React, { useState, useEffect } from 'react';
import { 
  Layout, 
  Menu, 
  Typography, 
  Button, 
  Space, 
  Table, 
  Tag, 
  Modal, 
  Card,
  Alert,
  Spin,
  Empty,
  message
} from 'antd';
import { 
  FileTextOutlined, 
  ExclamationCircleOutlined, 
  QuestionCircleOutlined,
  LogoutOutlined,
  HomeOutlined,
  WarningOutlined,
  CheckCircleOutlined,
  FileSearchOutlined,
  LoadingOutlined
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useContract } from '../contexts/ContractContext';
import ContractDetails from '../components/ContractDetails';
import ContractRow from '../components/ContractRow';
import AppHeader from '../components/AppHeader';
import ReactMarkdown from 'react-markdown';

const { Header, Sider, Content } = Layout;
const { Title, Text, Paragraph } = Typography;

const ExpiringContracts = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const { contracts, loading } = useContract();
  const [selectedContract, setSelectedContract] = useState(null);
  const [reportModalVisible, setReportModalVisible] = useState(false);
  const [generatingReport, setGeneratingReport] = useState(false);
  const [contractReport, setContractReport] = useState(null);

  // No need to load expiring contracts separately, we use all contracts for demo

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    {
      key: '/dashboard',
      icon: <HomeOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/contracts',
      icon: <FileTextOutlined />,
      label: 'All Contracts',
    },
    {
      key: '/expiring',
      icon: <ExclamationCircleOutlined />,
      label: 'Expiring Contracts',
    },
    {
      key: '/help',
      icon: <QuestionCircleOutlined />,
      label: 'Help & Support',
    },
  ];

  const handleMenuClick = ({ key }) => {
    navigate(key);
  };

  const getContractStatus = (contract) => {
    if (!contract.contract_end_date) {
      return { text: 'Missing End Date', color: 'purple', icon: <WarningOutlined /> };
    }
    
    const now = new Date();
    const endDate = new Date(contract.contract_end_date);
    const daysUntilExpiry = Math.ceil((endDate - now) / (1000 * 60 * 60 * 24));
    
    if (daysUntilExpiry < 0) {
      return { text: 'Expired', color: 'red', icon: <WarningOutlined /> };
    } else if (daysUntilExpiry <= 30) {
      return { text: 'Expiring Soon', color: 'orange', icon: <ExclamationCircleOutlined /> };
    } else {
      return { text: 'Active', color: 'green', icon: <CheckCircleOutlined /> };
    }
  };

  const handleGenerateReport = async (contract) => {
    try {
      setSelectedContract(contract);
      setReportModalVisible(true);
      setGeneratingReport(true);
      setContractReport(null);

      // Call new API to generate report for specific contract
      const response = await fetch(
        `http://localhost:8000/api/v1/contracts/report/${contract.id}?user_email=${user.email}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate report');
      }

      const result = await response.json();
      
      if (result.success) {
        setContractReport(result);
        message.success('Report generated successfully!');
      } else {
        message.warning('No report available for this contract');
      }

    } catch (error) {
      console.error('Error generating report:', error);
      message.error(`Failed to generate report: ${error.message}`);
    } finally {
      setGeneratingReport(false);
    }
  };

  const columns = [
    {
      title: 'Contract ID',
      dataIndex: 'id',
      key: 'id',
      width: 120,
      render: (text) => (
        <Text code style={{ fontSize: '12px' }}>
          {text ? text.slice(0, 8) + '...' : 'N/A'}
        </Text>
      ),
    },
    {
      title: 'Contract Information',
      dataIndex: 'service_name',
      key: 'contract_info',
      width: 500,
      render: (text, record) => <ContractRow contract={record} showDetails={true} />,
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button 
            type="primary" 
            icon={<FileSearchOutlined />}
            onClick={() => handleGenerateReport(record)}
          >
            Generate Report
          </Button>
        </Space>
      ),
    },
  ];

  const getAlertMessage = () => {
    return `Viewing all ${contracts.length} contracts. Click "Generate Report" to analyze any contract with AI.`;
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <AppHeader user={user} onLogout={logout} />

      <Layout>

        <Content style={{ margin: '24px', padding: '24px', background: '#fff', borderRadius: '8px' }}>
          <div style={{ marginBottom: '24px' }}>
            <Title level={2} style={{ color: '#2c3e50', fontWeight: '600' }}>Contract Analysis & Reports</Title>
            <Alert
              message={getAlertMessage()}
              type="info"
              showIcon
              style={{ marginBottom: '16px', borderRadius: '8px' }}
              description="Demo mode: All contracts are displayed. Use the 'Generate Report' button to get AI-powered analysis for any contract."
            />
          </div>

          {loading ? (
            <div style={{ textAlign: 'center', padding: '50px' }}>
              <Spin size="large" />
              <div style={{ marginTop: '16px' }}>Loading contracts...</div>
            </div>
          ) : contracts.length === 0 ? (
            <Empty
              description="No contracts available"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            />
          ) : (
            <Table
              columns={columns}
              dataSource={contracts}
              rowKey="id"
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} contracts`,
              }}
            />
          )}

          <Modal
            title={
              <Space>
                <FileSearchOutlined />
                <span>AI-Powered Contract Analysis Report</span>
              </Space>
            }
            open={reportModalVisible}
            onCancel={() => {
              setReportModalVisible(false);
              setContractReport(null);
              setSelectedContract(null);
            }}
            footer={[
              <Button 
                key="close" 
                type="primary"
                onClick={() => {
                  setReportModalVisible(false);
                  setContractReport(null);
                  setSelectedContract(null);
                }}
              >
                Close
              </Button>
            ]}
            width={1200}
            style={{ top: 20 }}
          >
            {selectedContract && (
              <div>
                <Card 
                  title="Contract Information" 
                  size="small" 
                  style={{ marginBottom: 16 }}
                >
                  <ContractDetails contract={selectedContract} showFullDetails={true} />
                </Card>
                
                <Card 
                  title={
                    <Space>
                      <FileSearchOutlined />
                      <span>AI Analysis & Recommendations</span>
                    </Space>
                  }
                  extra={
                    contractReport && (
                      <Tag color={
                        contractReport.expired_status === 'expired' ? 'red' : 
                        contractReport.expired_status === 'near_expiry' ? 'orange' : 
                        'blue'
                      }>
                        {contractReport.expired_status === 'expired' ? 'Expired' : 
                         contractReport.expired_status === 'near_expiry' ? 'Expiring Soon' : 
                         'Missing End Date'}
                      </Tag>
                    )
                  }
                >
                  {generatingReport ? (
                    <div style={{ textAlign: 'center', padding: '50px' }}>
                      <Spin 
                        indicator={<LoadingOutlined style={{ fontSize: 48 }} spin />}
                        size="large" 
                      />
                      <div style={{ marginTop: 24, fontSize: '16px', color: '#666' }}>
                        🤖 AI is analyzing the contract...
                      </div>
                      <div style={{ marginTop: 8, fontSize: '14px', color: '#999' }}>
                        This may take 30-60 seconds
                      </div>
                    </div>
                  ) : contractReport ? (
                    <div 
                      style={{ 
                        maxHeight: '600px', 
                        overflowY: 'auto',
                        padding: '16px',
                        background: '#fafafa',
                        borderRadius: '8px'
                      }}
                    >
                      <ReactMarkdown
                        components={{
                          h1: ({node, ...props}) => <h2 style={{ color: '#1890ff', marginTop: '24px', marginBottom: '16px' }} {...props} />,
                          h2: ({node, ...props}) => <h3 style={{ color: '#2c3e50', marginTop: '20px', marginBottom: '12px' }} {...props} />,
                          h3: ({node, ...props}) => <h4 style={{ color: '#2c3e50', marginTop: '16px', marginBottom: '8px' }} {...props} />,
                          p: ({node, ...props}) => <p style={{ lineHeight: '1.8', marginBottom: '12px', color: '#333' }} {...props} />,
                          ul: ({node, ...props}) => <ul style={{ lineHeight: '1.8', marginBottom: '12px', paddingLeft: '24px' }} {...props} />,
                          ol: ({node, ...props}) => <ol style={{ lineHeight: '1.8', marginBottom: '12px', paddingLeft: '24px' }} {...props} />,
                          li: ({node, ...props}) => <li style={{ marginBottom: '8px' }} {...props} />,
                          strong: ({node, ...props}) => <strong style={{ color: '#1890ff', fontWeight: '600' }} {...props} />,
                          code: ({node, inline, ...props}) => 
                            inline ? 
                              <code style={{ background: '#f0f0f0', padding: '2px 6px', borderRadius: '4px', color: '#d63384' }} {...props} /> :
                              <code style={{ display: 'block', background: '#f5f5f5', padding: '12px', borderRadius: '6px', overflowX: 'auto' }} {...props} />
                        }}
                      >
                        {contractReport.report || 'No report available'}
                      </ReactMarkdown>
                    </div>
                  ) : (
                    <Empty 
                      description="Report generation failed. Please try again."
                      image={Empty.PRESENTED_IMAGE_SIMPLE}
                    />
                  )}
                </Card>
              </div>
            )}
          </Modal>
        </Content>
      </Layout>
    </Layout>
  );
};

export default ExpiringContracts;
