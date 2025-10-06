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
  Empty
} from 'antd';
import { 
  FileTextOutlined, 
  ExclamationCircleOutlined, 
  QuestionCircleOutlined,
  LogoutOutlined,
  HomeOutlined,
  WarningOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useContract } from '../contexts/ContractContext';
import ContractDetails from '../components/ContractDetails';
import ContractRow from '../components/ContractRow';
import AppHeader from '../components/AppHeader';

const { Header, Sider, Content } = Layout;
const { Title, Text, Paragraph } = Typography;

const ExpiringContracts = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const { expiringContracts, loading, loadExpiringContracts } = useContract();
  const [selectedContract, setSelectedContract] = useState(null);
  const [reportModalVisible, setReportModalVisible] = useState(false);

  useEffect(() => {
    if (user?.email) {
      loadExpiringContracts();
    }
  }, [user?.email, loadExpiringContracts]);

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

  const handleViewReport = (contract) => {
    setSelectedContract(contract);
    setReportModalVisible(true);
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
      render: (_, record) => (
        <Space>
          <Button 
            type="primary" 
            onClick={() => handleViewReport(record)}
          >
            View AI Report
          </Button>
        </Space>
      ),
    },
  ];

  const getAlertType = () => {
    if (expiringContracts.length === 0) return 'success';
    
    const hasExpired = expiringContracts.some(c => {
      if (!c.contract_end_date) return false;
      const endDate = new Date(c.contract_end_date);
      return endDate < new Date();
    });
    
    const hasExpiring = expiringContracts.some(c => {
      if (!c.contract_end_date) return false;
      const now = new Date();
      const endDate = new Date(c.contract_end_date);
      const daysUntilExpiry = Math.ceil((endDate - now) / (1000 * 60 * 60 * 24));
      return daysUntilExpiry <= 30 && daysUntilExpiry >= 0;
    });
    
    if (hasExpired) return 'error';
    if (hasExpiring) return 'warning';
    return 'info';
  };

  const getAlertMessage = () => {
    if (expiringContracts.length === 0) {
      return 'Great! No contracts need attention.';
    }
    
    const expiredCount = expiringContracts.filter(c => {
      if (!c.contract_end_date) return false;
      const endDate = new Date(c.contract_end_date);
      return endDate < new Date();
    }).length;
    
    const expiringCount = expiringContracts.filter(c => {
      if (!c.contract_end_date) return false;
      const now = new Date();
      const endDate = new Date(c.contract_end_date);
      const daysUntilExpiry = Math.ceil((endDate - now) / (1000 * 60 * 60 * 24));
      return daysUntilExpiry <= 30 && daysUntilExpiry >= 0;
    }).length;
    
    const missingDateCount = expiringContracts.filter(c => !c.contract_end_date).length;
    
    let message = `${expiringContracts.length} contracts need attention: `;
    const parts = [];
    
    if (expiredCount > 0) parts.push(`${expiredCount} expired`);
    if (expiringCount > 0) parts.push(`${expiringCount} expiring soon`);
    if (missingDateCount > 0) parts.push(`${missingDateCount} missing end date`);
    
    return message + parts.join(', ');
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <AppHeader user={user} onLogout={logout} />

      <Layout>

        <Content style={{ margin: '24px', padding: '24px', background: '#fff', borderRadius: '8px' }}>
          <div style={{ marginBottom: '24px' }}>
            <Title level={2} style={{ color: '#2c3e50', fontWeight: '600' }}>Contract Alerts</Title>
            <Alert
              message={getAlertMessage()}
              type={getAlertType()}
              showIcon
              style={{ marginBottom: '16px', borderRadius: '8px' }}
            />
          </div>

          {loading ? (
            <div style={{ textAlign: 'center', padding: '50px' }}>
              <Spin size="large" />
              <div style={{ marginTop: '16px' }}>Loading data...</div>
            </div>
          ) : expiringContracts.length === 0 ? (
            <Empty
              description="No contracts need attention"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            />
          ) : (
            <Table
              columns={columns}
              dataSource={expiringContracts}
              rowKey="contract_id"
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} contracts`,
              }}
            />
          )}

          <Modal
            title="AI Report - Contract Analysis"
            open={reportModalVisible}
            onCancel={() => setReportModalVisible(false)}
            footer={[
              <Button key="close" onClick={() => setReportModalVisible(false)}>
                Close
              </Button>
            ]}
            width={1000}
            style={{ top: 20 }}
          >
            {selectedContract && (
              <div>
                <ContractDetails contract={selectedContract} showFullDetails={true} />
                
                <Card title="AI Analysis Report" size="small">
                  <div 
                    style={{ 
                      maxHeight: '500px', 
                      overflowY: 'auto',
                      whiteSpace: 'pre-wrap',
                      fontFamily: 'monospace',
                      fontSize: '12px',
                      lineHeight: '1.5'
                    }}
                    dangerouslySetInnerHTML={{ 
                      __html: selectedContract.report?.replace(/\n/g, '<br>') || 'No report available' 
                    }}
                  />
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
