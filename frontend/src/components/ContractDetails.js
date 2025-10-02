import React from 'react';
import { Card, Typography, Divider, Tag, Space } from 'antd';
import { CalendarOutlined, UserOutlined, BankOutlined, FileTextOutlined, LinkOutlined } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

const ContractDetails = ({ contract, showFullDetails = false }) => {
  if (!contract) return null;

  const formatDate = (dateString) => {
    if (!dateString) return 'Not specified';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  const getContractStatus = (contract) => {
    if (!contract.contract_end_date) {
      return { text: 'Missing End Date', color: 'purple' };
    }
    
    const now = new Date();
    const endDate = new Date(contract.contract_end_date);
    const daysUntilExpiry = Math.ceil((endDate - now) / (1000 * 60 * 60 * 24));
    
    if (daysUntilExpiry < 0) {
      return { text: 'Expired', color: 'red' };
    } else if (daysUntilExpiry <= 30) {
      return { text: 'Expiring Soon', color: 'orange' };
    } else {
      return { text: 'Active', color: 'green' };
    }
  };

  const status = getContractStatus(contract);

  return (
    <Card 
      size="small" 
      style={{ 
        marginBottom: '16px',
        borderRadius: '8px',
        border: '1px solid #f0f0f0'
      }}
    >
      <div style={{ marginBottom: '12px' }}>
        <Space align="center">
          <FileTextOutlined style={{ color: '#8B4513' }} />
          <Title level={5} style={{ margin: 0, color: '#2c3e50' }}>
            {contract.service_name || 'Unnamed Service'}
          </Title>
          <Tag color={status.color}>{status.text}</Tag>
        </Space>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        <div>
          <Space direction="vertical" size="small" style={{ width: '100%' }}>
            <div>
              <Text strong style={{ color: '#666' }}>Contract ID:</Text>
              <br />
              <Text code style={{ fontSize: '12px' }}>
                {contract.id ? contract.id.slice(0, 8) + '...' : 'N/A'}
              </Text>
            </div>

            <div>
              <Space>
                <BankOutlined style={{ color: '#8B4513' }} />
                <div>
                  <Text strong style={{ color: '#666' }}>Supplier:</Text>
                  <br />
                  <Text>{contract.supplier_name || 'Not specified'}</Text>
                </div>
              </Space>
            </div>

            <div>
              <Space>
                <UserOutlined style={{ color: '#8B4513' }} />
                <div>
                  <Text strong style={{ color: '#666' }}>Customer:</Text>
                  <br />
                  <Text>{contract.customer_name || 'Not specified'}</Text>
                </div>
              </Space>
            </div>
          </Space>
        </div>

        <div>
          <Space direction="vertical" size="small" style={{ width: '100%' }}>
            <div>
              <Space>
                <CalendarOutlined style={{ color: '#8B4513' }} />
                <div>
                  <Text strong style={{ color: '#666' }}>Start Date:</Text>
                  <br />
                  <Text>{formatDate(contract.contract_start_date)}</Text>
                </div>
              </Space>
            </div>

            <div>
              <Space>
                <CalendarOutlined style={{ color: '#8B4513' }} />
                <div>
                  <Text strong style={{ color: '#666' }}>End Date:</Text>
                  <br />
                  <Text>{formatDate(contract.contract_end_date)}</Text>
                </div>
              </Space>
            </div>

            <div>
              <Text strong style={{ color: '#666' }}>Notice Period:</Text>
              <br />
              <Text style={{ fontSize: '12px' }}>
                {contract.termination_notice_period || 'Not specified'}
              </Text>
            </div>
          </Space>
        </div>
      </div>

      {showFullDetails && (
        <>
          <Divider style={{ margin: '16px 0' }} />
          
          <div>
            <Text strong style={{ color: '#666' }}>Contract Details:</Text>
            <div style={{ 
              background: '#f8f9fa', 
              padding: '12px', 
              borderRadius: '6px',
              marginTop: '8px',
              maxHeight: '200px',
              overflowY: 'auto',
              fontSize: '13px',
              lineHeight: '1.6',
              border: '1px solid #e9ecef'
            }}>
              <Text style={{ whiteSpace: 'pre-wrap' }}>
                {contract.contract_details || 'Not specified'}
              </Text>
            </div>
          </div>

          {contract.LinkImage && (
            <div style={{ marginTop: '12px' }}>
              <Space>
                <LinkOutlined style={{ color: '#8B4513' }} />
                <Text strong style={{ color: '#666' }}>Document:</Text>
                <a 
                  href={contract.LinkImage} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style={{ color: '#1890ff' }}
                >
                  View Document
                </a>
              </Space>
            </div>
          )}

          <div style={{ marginTop: '12px', fontSize: '12px', color: '#999' }}>
            <Text>Created: {formatDate(contract.created_at)}</Text>
            <br />
            <Text>Updated: {formatDate(contract.updated_at)}</Text>
          </div>
        </>
      )}
    </Card>
  );
};

export default ContractDetails;
