import React, { useState } from 'react';
import { 
  Layout, 
  Menu, 
  Typography, 
  Button, 
  Space, 
  Table, 
  Tag, 
  Modal, 
  Form, 
  Input, 
  DatePicker, 
  message,
  Popconfirm,
  Tabs
} from 'antd';
import {
  FileTextOutlined,
  ExclamationCircleOutlined,
  QuestionCircleOutlined,
  LogoutOutlined,
  HomeOutlined,
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  ShopOutlined,
  UserOutlined,
  UploadOutlined,
  FormOutlined
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useContract } from '../contexts/ContractContext';
import ContractDetails from '../components/ContractDetails';
import ContractRow from '../components/ContractRow';
import AppHeader from '../components/AppHeader';
import ResizableTable from '../components/ResizableTable';
import ContractUpload from '../components/ContractUpload';
import dayjs from 'dayjs';

const { Header, Sider, Content } = Layout;
const { Title, Text } = Typography;
const { TextArea } = Input;

const AllContracts = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const { contracts, loading, createContract, updateContract, deleteContract, refreshContracts } = useContract();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isUploadModalVisible, setIsUploadModalVisible] = useState(false);
  const [editingContract, setEditingContract] = useState(null);
  const [form] = Form.useForm();

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
    if (!contract.contract_end_date) return { status: 'unknown', text: 'Unknown', color: 'orange' };
    
    const endDate = dayjs(contract.contract_end_date);
    const now = dayjs();
    const diffDays = endDate.diff(now, 'day');
    
    if (diffDays < 0) return { status: 'expired', text: 'Expired', color: 'red' };
    if (diffDays <= 60) return { status: 'expiring', text: 'Expiring Soon', color: 'orange' };
    return { status: 'valid', text: 'Active', color: 'green' };
  };

  const handleAddContract = () => {
    setIsUploadModalVisible(true);
  };

  const handleManualAddContract = () => {
    setEditingContract(null);
    form.resetFields();
    setIsModalVisible(true);
    setIsUploadModalVisible(false);
  };

  const handleUploadSuccess = (result) => {
    message.success('Contract uploaded and extracted successfully!');
    refreshContracts();
    setIsUploadModalVisible(false);
  };

  const handleEditContract = (contract) => {
    setEditingContract(contract);
    form.setFieldsValue({
      ...contract,
      contract_start_date: contract.contract_start_date ? dayjs(contract.contract_start_date) : null,
      contract_end_date: contract.contract_end_date ? dayjs(contract.contract_end_date) : null,
    });
    setIsModalVisible(true);
  };

  const handleDeleteContract = async (contractId) => {
    const result = await deleteContract(contractId);
    if (result.success) {
      message.success('Contract deleted successfully');
    } else {
      message.error(result.message);
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      const contractData = {
        ...values,
        contract_start_date: values.contract_start_date ? values.contract_start_date.format('YYYY/MM/DD') : null,
        contract_end_date: values.contract_end_date ? values.contract_end_date.format('YYYY/MM/DD') : null,
      };

      if (editingContract) {
        const result = await updateContract(editingContract.id, contractData);
      if (result.success) {
        message.success('Contract updated successfully');
        setIsModalVisible(false);
      } else {
        message.error(result.message);
      }
    } else {
      contractData.id = `contract_${Date.now()}`;
      const result = await createContract(contractData);
      if (result.success) {
        message.success('Contract created successfully');
        setIsModalVisible(false);
      } else {
        message.error(result.message);
      }
    }
    } catch (error) {
      console.error('Form validation failed:', error);
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 120,
      fixed: 'left',
      render: (text) => (
        <Text code style={{ fontSize: '12px' }}>
          {text ? text.slice(0, 10) + '...' : 'N/A'}
        </Text>
      ),
    },
    {
      title: 'Service Name',
      dataIndex: 'service_name',
      key: 'service_name',
      width: 250,
      render: (text, record) => {
        const status = getContractStatus(record);
        return (
          <div>
            <div style={{ marginBottom: '6px' }}>
              <Text strong style={{ fontSize: '14px', color: '#2c3e50' }}>
                {text || 'Unnamed Service'}
              </Text>
            </div>
            <Tag color={status.color} style={{ fontSize: '11px' }}>
              {status.text}
            </Tag>
          </div>
        );
      },
    },
    {
      title: 'Supplier',
      dataIndex: 'supplier_name',
      key: 'supplier_name',
      width: 220,
      render: (text) => (
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <ShopOutlined style={{ color: '#8B4513', fontSize: '14px' }} />
          <Text style={{ fontSize: '13px' }} ellipsis={{ tooltip: text }}>
            {text || 'Not specified'}
          </Text>
        </div>
      ),
    },
    {
      title: 'Customer',
      dataIndex: 'customer_name',
      key: 'customer_name',
      width: 220,
      render: (text) => (
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <UserOutlined style={{ color: '#8B4513', fontSize: '14px' }} />
          <Text style={{ fontSize: '13px' }} ellipsis={{ tooltip: text }}>
            {text || 'Not specified'}
          </Text>
        </div>
      ),
    },
    {
      title: 'Start Date',
      dataIndex: 'contract_start_date',
      key: 'contract_start_date',
      width: 120,
      render: (text) => (
        <Text style={{ fontSize: '13px' }}>
          {text || 'Not specified'}
        </Text>
      ),
    },
    {
      title: 'End Date',
      dataIndex: 'contract_end_date',
      key: 'contract_end_date',
      width: 120,
      render: (text) => (
        <Text style={{ fontSize: '13px' }}>
          {text || 'Not specified'}
        </Text>
      ),
    },
    {
      title: 'Contract Details',
      dataIndex: 'contract_details',
      key: 'contract_details',
      width: 250,
      render: (text) => (
        <Text 
          ellipsis={{ 
            tooltip: text,
            rows: 3 
          }}
          style={{ 
            fontSize: '12px',
            lineHeight: '1.5',
            color: '#666'
          }}
        >
          {text || 'Not specified'}
        </Text>
      ),
    },
    {
      title: 'Notice Period',
      dataIndex: 'termination_notice_period',
      key: 'termination_notice_period',
      width: 200,
      render: (text) => (
        <Text 
          ellipsis={{ 
            tooltip: text,
            rows: 2 
          }}
          style={{ 
            fontSize: '12px',
            lineHeight: '1.5'
          }}
        >
          {text || 'Not specified'}
        </Text>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 180,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small">
          <Button 
            type="link" 
            size="small"
            icon={<EyeOutlined />}
            onClick={() => {
              Modal.info({
                title: 'Contract Details',
                content: <ContractDetails contract={record} showFullDetails={true} />,
                width: 800,
              });
            }}
          >
            View
          </Button>
          <Button 
            type="link" 
            size="small"
            icon={<EditOutlined />} 
            onClick={() => handleEditContract(record)}
          >
            Edit
          </Button>
          <Popconfirm
            title="Are you sure you want to delete this contract?"
            onConfirm={() => handleDeleteContract(record.id)}
            okText="Yes"
            cancelText="No"
          >
            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
              Delete
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <AppHeader user={user} onLogout={logout} />

      <Layout>

        <Content style={{ margin: '24px', padding: '24px', background: '#fff', borderRadius: '8px' }}>
          <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Title level={2} style={{ margin: 0, color: '#2c3e50', fontWeight: '600' }}>Contract List</Title>
            <Space>
              <Button 
                type="default" 
                icon={<FormOutlined />} 
                onClick={handleManualAddContract}
                style={{ borderRadius: '8px' }}
              >
                Manual Entry
              </Button>
              <Button 
                type="primary" 
                icon={<UploadOutlined />} 
                onClick={handleAddContract}
                style={{ borderRadius: '8px' }}
              >
                Upload Contract
              </Button>
            </Space>
          </div>

          <ResizableTable
            columns={columns}
            dataSource={contracts}
            rowKey="id"
            loading={loading}
            pagination={{
              pageSize: 10,
              showSizeChanger: true,
              showQuickJumper: true,
              showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} contracts`,
            }}
            scroll={{ x: 1700 }}
            size="middle"
            bordered={false}
            style={{ 
              background: '#fff',
              borderRadius: '8px',
              overflow: 'hidden'
            }}
          />

          <ContractUpload
            visible={isUploadModalVisible}
            onClose={() => setIsUploadModalVisible(false)}
            onSuccess={handleUploadSuccess}
            userEmail={user?.email}
          />

          <Modal
            title={editingContract ? 'Edit Contract' : 'Manual Contract Entry'}
            open={isModalVisible}
            onOk={handleModalOk}
            onCancel={() => setIsModalVisible(false)}
            width={800}
            okText="Save"
            cancelText="Cancel"
          >
            <Form
              form={form}
              layout="vertical"
              initialValues={editingContract}
            >
              <Form.Item
                name="service_name"
                label="Service Name"
                rules={[{ required: true, message: 'Please enter service name!' }]}
              >
                <Input placeholder="Enter service name" />
              </Form.Item>

              <Form.Item
                name="supplier_name"
                label="Supplier"
                rules={[{ required: true, message: 'Please enter supplier name!' }]}
              >
                <Input placeholder="Enter supplier name" />
              </Form.Item>

              <Form.Item
                name="customer_name"
                label="Customer"
                rules={[{ required: true, message: 'Please enter customer name!' }]}
              >
                <Input placeholder="Enter customer name" />
              </Form.Item>

                     <Form.Item
                       name="contract_start_date"
                       label="Start Date"
                     >
                       <DatePicker 
                         style={{ width: '100%' }} 
                         format="YYYY/MM/DD" 
                         placeholder="Select start date"
                       />
                     </Form.Item>
       
                     <Form.Item
                       name="contract_end_date"
                       label="End Date"
                     >
                       <DatePicker 
                         style={{ width: '100%' }} 
                         format="YYYY/MM/DD" 
                         placeholder="Select end date"
                       />
                     </Form.Item>

              <Form.Item
                name="contract_details"
                label="Contract Details"
              >
                <TextArea rows={4} placeholder="Enter contract details" />
              </Form.Item>

              <Form.Item
                name="termination_notice_period"
                label="Notice Period"
              >
                <Input placeholder="Enter notice period" />
              </Form.Item>

              <Form.Item
                name="LinkImage"
                label="Image Link"
              >
                <Input placeholder="Enter image link" />
              </Form.Item>
            </Form>
          </Modal>
        </Content>
      </Layout>
    </Layout>
  );
};

export default AllContracts;
