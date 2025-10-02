import React from 'react';
import { Layout, Typography, Menu, Button, Space } from 'antd';
import { 
  LogoutOutlined, 
  HomeOutlined, 
  FileTextOutlined, 
  ExclamationCircleOutlined, 
  QuestionCircleOutlined 
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';

const { Header } = Layout;
const { Title, Text } = Typography;

const AppHeader = ({ user, onLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();

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

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  return (
    <Header style={{ 
      background: 'linear-gradient(135deg, #8B4513 0%, #A0522D 100%)',
      padding: '0',
      boxShadow: '0 4px 20px rgba(139, 69, 19, 0.3)',
      border: 'none',
      position: 'sticky',
      top: 0,
      zIndex: 1000
    }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        height: '70px',
        padding: '0 32px',
        maxWidth: '1400px',
        margin: '0 auto'
      }}>
        {/* Logo Section */}
        <div style={{ 
          display: 'flex',
          alignItems: 'center',
          gap: '12px'
        }}>
          <div style={{
            width: '40px',
            height: '40px',
            background: 'rgba(255, 255, 255, 0.2)',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            overflow: 'hidden'
          }}>
            <img 
              src="/star-logo.png" 
              alt="SaaSeer Logo" 
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover'
              }}
            />
          </div>
          <div>
            <Title level={3} style={{ 
              margin: 0, 
              color: '#fff', 
              fontWeight: '700',
              fontSize: '24px',
              lineHeight: '1.2'
            }}>
              SaaSeer
            </Title>
            <Text style={{ 
              color: 'rgba(255, 255, 255, 0.8)', 
              fontSize: '12px',
              fontWeight: '400',
              display: 'block',
              marginTop: '-4px'
            }}>
              Contract Management
            </Text>
          </div>
        </div>

        {/* Navigation Menu */}
        <Menu
          mode="horizontal"
          selectedKeys={[location.pathname]}
          onClick={handleMenuClick}
          items={menuItems.map(item => ({
            ...item,
            style: {
              color: 'rgba(255, 255, 255, 0.9)',
              fontWeight: '500',
              height: '50px',
              lineHeight: '50px',
              padding: '0 20px',
              borderRadius: '8px',
              margin: '0 4px',
              transition: 'all 0.3s ease'
            }
          }))}
          style={{ 
            background: 'transparent',
            border: 'none',
            flex: 1,
            justifyContent: 'center',
            margin: '0 40px'
          }}
          theme="dark"
        />

        {/* User Section */}
        <div style={{ 
          display: 'flex',
          alignItems: 'center',
          gap: '16px'
        }}>
          <div className="user-profile-card" style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 16px',
            background: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '20px',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            transition: 'all 0.3s ease',
            cursor: 'pointer'
          }}>
            <div style={{
              width: '32px',
              height: '32px',
              background: 'rgba(255, 255, 255, 0.2)',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '14px',
              fontWeight: 'bold',
              color: '#fff'
            }}>
              {user?.email?.charAt(0).toUpperCase() || 'U'}
            </div>
            <Text style={{ 
              color: '#fff', 
              fontWeight: '500',
              fontSize: '14px'
            }}>
              {user?.email?.split('@')[0] || 'User'}
            </Text>
          </div>
          
          <Button 
            type="text"
            icon={<LogoutOutlined />} 
            onClick={handleLogout}
            className="sign-out-btn"
            style={{ 
              color: 'rgba(255, 255, 255, 0.9)',
              border: '1px solid rgba(255, 255, 255, 0.3)',
              borderRadius: '8px',
              height: '40px',
              padding: '0 16px',
              background: 'rgba(255, 255, 255, 0.1)',
              transition: 'all 0.3s ease'
            }}
          >
            Sign Out
          </Button>
        </div>
      </div>
    </Header>
  );
};

export default AppHeader;
