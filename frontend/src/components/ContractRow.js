import React from 'react';
import { Tag, Tooltip, Space } from 'antd';
import { CalendarOutlined, UserOutlined, BankOutlined } from '@ant-design/icons';

const ContractRow = ({ contract, showDetails = true }) => {
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
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
          <strong style={{ color: '#2c3e50', fontSize: '14px' }}>
            {contract.service_name || 'Unnamed Service'}
          </strong>
          <Tag color={status.color} size="small">{status.text}</Tag>
        </div>
        
        <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: '#666' }}>
          <Space size="small">
            <BankOutlined />
            <span>{contract.supplier_name || 'No supplier'}</span>
          </Space>
          
          <Space size="small">
            <UserOutlined />
            <span>{contract.customer_name || 'No customer'}</span>
          </Space>
          
          <Space size="small">
            <CalendarOutlined />
            <span>{contract.contract_end_date || 'No end date'}</span>
          </Space>
        </div>

        {showDetails && contract.contract_details && (
          <Tooltip title={contract.contract_details} placement="top">
            <div style={{ 
              marginTop: '4px',
              fontSize: '11px',
              color: '#999',
              maxWidth: '300px',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap'
            }}>
              {contract.contract_details.length > 60 
                ? contract.contract_details.substring(0, 60) + '...'
                : contract.contract_details
              }
            </div>
          </Tooltip>
        )}
      </div>
    </div>
  );
};

export default ContractRow;
