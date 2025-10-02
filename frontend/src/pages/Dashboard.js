import React from 'react';
import { Layout, Menu, Typography, Button, Space, Card, Row, Col, Statistic } from 'antd';
import { 
  FileTextOutlined, 
  ExclamationCircleOutlined, 
  QuestionCircleOutlined,
  LogoutOutlined,
  HomeOutlined
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useContract } from '../contexts/ContractContext';
import ApiStatus from '../components/ApiStatus';
import ApiTester from '../components/ApiTester';
import ContractDetails from '../components/ContractDetails';
import ContractStats from '../components/ContractStats';
import AppHeader from '../components/AppHeader';

const { Header, Sider, Content } = Layout;
const { Title, Text } = Typography;

const Dashboard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const { contracts, expiringContracts, loading } = useContract();

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
    if (!contract.contract_end_date) return { status: 'unknown', text: 'Unknown', color: '#faad14' };
    
    const endDate = new Date(contract.contract_end_date);
    const now = new Date();
    const diffTime = endDate - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return { status: 'expired', text: 'Expired', color: '#ff4d4f' };
    if (diffDays <= 60) return { status: 'expiring', text: 'Expiring Soon', color: '#faad14' };
    return { status: 'valid', text: 'Active', color: '#52c41a' };
  };

  const validContracts = contracts.filter(c => getContractStatus(c).status === 'valid').length;
  const expiringCount = contracts.filter(c => getContractStatus(c).status === 'expiring').length;

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <AppHeader user={user} onLogout={logout} />

      <Layout>

        <Content style={{ 
          margin: '24px', 
          padding: '32px', 
          background: '#fff', 
          borderRadius: '16px',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
          border: '1px solid #f0f0f0'
        }}>
          <ApiStatus />
          <ApiTester />
          <Title level={2} style={{ marginBottom: '32px', color: '#2c3e50', fontWeight: '600' }}>
            System Overview
          </Title>
          
          <ContractStats contracts={contracts} expiringContracts={expiringContracts} />

          <Row gutter={[24, 24]}>
            <Col xs={24} lg={12}>
              <Card 
                title="Recent Contracts" 
                extra={<Button type="link" onClick={() => navigate('/contracts')} style={{ color: '#8B4513', fontWeight: '500' }}>View All</Button>}
                style={{ 
                  borderRadius: '12px', 
                  border: 'none',
                  boxShadow: '0 2px 12px rgba(0, 0, 0, 0.06)'
                }}
              >
                {loading ? (
                  <div style={{ textAlign: 'center', padding: '20px' }}>Loading...</div>
                ) : contracts.length > 0 ? (
                  <div>
                    {contracts.slice(0, 3).map((contract) => (
                      <ContractDetails 
                        key={contract.id} 
                        contract={contract} 
                        showFullDetails={false}
                      />
                    ))}
                    {contracts.length > 3 && (
                      <div style={{ textAlign: 'center', marginTop: '12px' }}>
                        <Button 
                          type="link" 
                          onClick={() => navigate('/contracts')}
                          style={{ color: '#8B4513' }}
                        >
                          View All Contracts ({contracts.length})
                        </Button>
                      </div>
                    )}
                  </div>
                ) : (
                  <Text type="secondary" style={{ textAlign: 'center', display: 'block', padding: '20px' }}>No contracts yet</Text>
                )}
              </Card>
            </Col>
            
            <Col xs={24} lg={12}>
              <Card 
                title="Expiration Alerts" 
                extra={<Button type="link" onClick={() => navigate('/expiring')} style={{ color: '#8B4513', fontWeight: '500' }}>View Details</Button>}
                style={{ 
                  borderRadius: '12px', 
                  border: 'none',
                  boxShadow: '0 2px 12px rgba(0, 0, 0, 0.06)'
                }}
              >
                {loading ? (
                  <div style={{ textAlign: 'center', padding: '20px' }}>Loading...</div>
                ) : expiringContracts.length > 0 ? (
                  <div>
                    {expiringContracts.slice(0, 3).map((contract) => (
                      <ContractDetails 
                        key={contract.id} 
                        contract={contract} 
                        showFullDetails={false}
                      />
                    ))}
                    {expiringContracts.length > 3 && (
                      <div style={{ textAlign: 'center', marginTop: '12px' }}>
                        <Button 
                          type="link" 
                          onClick={() => navigate('/expiring')}
                          style={{ color: '#8B4513' }}
                        >
                          View All Expiring ({expiringContracts.length})
                        </Button>
                      </div>
                    )}
                  </div>
                ) : (
                  <Text type="secondary" style={{ textAlign: 'center', display: 'block', padding: '20px' }}>No alerts</Text>
                )}
              </Card>
            </Col>
          </Row>
        </Content>
      </Layout>
    </Layout>
  );
};

export default Dashboard;
