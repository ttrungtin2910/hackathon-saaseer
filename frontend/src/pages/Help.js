import React from 'react';
import { 
  Layout, 
  Menu, 
  Typography, 
  Button, 
  Space, 
  Card,
  List,
  Divider,
  Alert,
  Row,
  Col
} from 'antd';
import { 
  FileTextOutlined, 
  ExclamationCircleOutlined, 
  QuestionCircleOutlined,
  LogoutOutlined,
  HomeOutlined,
  PhoneOutlined,
  MailOutlined,
  GlobalOutlined,
  BookOutlined,
  SettingOutlined,
  TeamOutlined
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import AppHeader from '../components/AppHeader';

const { Header, Sider, Content } = Layout;
const { Title, Text, Paragraph } = Typography;

const Help = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

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

  const helpSections = [
    {
      title: 'User Guide',
      icon: <BookOutlined />,
      items: [
        'How to add new contracts',
        'How to edit contract information',
        'How to delete contracts',
        'How to view AI reports',
        'How to manage expiring contracts'
      ]
    },
    {
      title: 'Key Features',
      icon: <SettingOutlined />,
      items: [
        'Contract list management',
        'Expiring contract tracking',
        'Automatic AI reports',
        'Search and filter contracts',
        'Contract data export'
      ]
    },
    {
      title: 'Technical Support',
      icon: <TeamOutlined />,
      items: [
        'Contact development team',
        'Report system issues',
        'Request new features',
        'Installation guide',
        'API documentation'
      ]
    }
  ];

  const contactInfo = [
    {
      icon: <MailOutlined />,
      title: 'Support Email',
      content: 'support@saaseer.com'
    },
    {
      icon: <PhoneOutlined />,
      title: 'Hotline',
      content: '+84 123 456 789'
    },
    {
      icon: <GlobalOutlined />,
      title: 'Website',
      content: 'https://saaseer.com'
    }
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <AppHeader user={user} onLogout={logout} />

      <Layout>

        <Content style={{ margin: '24px', padding: '24px', background: '#fff', borderRadius: '8px' }}>
          <div style={{ marginBottom: '32px' }}>
            <Title level={2} style={{ color: '#2c3e50', fontWeight: '600' }}>Help Center</Title>
            <Paragraph style={{ fontSize: '16px', lineHeight: '1.6' }}>
              Welcome to the SaaSeer Contract Management System. 
              Here you can learn how to use the system features 
              and get support when needed.
            </Paragraph>
          </div>

          <Alert
            message="Important Notice"
            description="The system is currently in development. Some features may not be complete. Please contact the development team if you encounter any issues."
            type="info"
            showIcon
            style={{ marginBottom: '32px', borderRadius: '8px' }}
          />

          <div style={{ marginBottom: '32px' }}>
            <Title level={3} style={{ color: '#2c3e50', fontWeight: '600' }}>User Guide</Title>
            <Row gutter={[16, 16]}>
              {helpSections.map((section, index) => (
                <Col xs={24} md={8} key={index}>
                  <Card 
                    title={
                      <Space>
                        {section.icon}
                        {section.title}
                      </Space>
                    }
                    size="small"
                  >
                    <List
                      size="small"
                      dataSource={section.items}
                      renderItem={(item) => (
                        <List.Item>
                          <Text>• {item}</Text>
                        </List.Item>
                      )}
                    />
                  </Card>
                </Col>
              ))}
            </Row>
          </div>

          <Divider />

          <div style={{ marginBottom: '32px' }}>
            <Title level={3} style={{ color: '#2c3e50', fontWeight: '600' }}>Contact Support</Title>
            <Row gutter={[16, 16]}>
              {contactInfo.map((info, index) => (
                <Col xs={24} sm={8} key={index}>
                  <Card size="small">
                    <Space direction="vertical" style={{ width: '100%', textAlign: 'center' }}>
                      <div style={{ fontSize: '24px', color: '#1890ff' }}>
                        {info.icon}
                      </div>
                      <Text strong>{info.title}</Text>
                      <Text>{info.content}</Text>
                    </Space>
                  </Card>
                </Col>
              ))}
            </Row>
          </div>

          <Divider />

          <div>
            <Title level={3} style={{ color: '#2c3e50', fontWeight: '600' }}>Frequently Asked Questions (FAQ)</Title>
            <Card>
              <List
                dataSource={[
                  {
                    question: 'How do I add a new contract?',
                    answer: 'Go to the "All Contracts" page and click the "Add Contract" button. Fill in all the information and click "Save".'
                  },
                  {
                    question: 'Why can\'t I see contracts in the list?',
                    answer: 'Contracts are filtered by user email. Make sure you are logged in with the correct account.'
                  },
                  {
                    question: 'What is the AI report?',
                    answer: 'The AI report automatically analyzes expiring contracts and provides recommendations for alternative services.'
                  },
                  {
                    question: 'How do I update contract information?',
                    answer: 'In the contract list, click the "Edit" button in the "Actions" column to modify the information.'
                  },
                  {
                    question: 'Does the system support data export?',
                    answer: 'Data export feature is not currently available. This feature will be added in future versions.'
                  }
                ]}
                renderItem={(item) => (
                  <List.Item>
                    <div>
                      <Text strong style={{ color: '#8B4513' }}>Q: {item.question}</Text>
                      <br />
                      <Text>A: {item.answer}</Text>
                    </div>
                  </List.Item>
                )}
              />
            </Card>
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default Help;
