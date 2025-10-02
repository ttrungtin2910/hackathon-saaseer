import React from 'react';
import { Card, Statistic, Row, Col, Progress, Typography } from 'antd';
import { 
  FileTextOutlined, 
  CheckCircleOutlined, 
  ExclamationCircleOutlined, 
  WarningOutlined 
} from '@ant-design/icons';

const { Text } = Typography;

const ContractStats = ({ contracts, expiringContracts }) => {
  const totalContracts = contracts.length;
  const activeContracts = contracts.filter(contract => {
    if (!contract.contract_end_date) return false;
    const endDate = new Date(contract.contract_end_date);
    return endDate > new Date();
  }).length;
  
  const expiredContracts = contracts.filter(contract => {
    if (!contract.contract_end_date) return false;
    const endDate = new Date(contract.contract_end_date);
    return endDate < new Date();
  }).length;
  
  const expiringSoon = expiringContracts.length;
  
  // Calculate contract value statistics (if available in contract_details)
  const contractsWithValue = contracts.filter(contract => 
    contract.contract_details && 
    contract.contract_details.includes('月額')
  );
  
  const totalMonthlyValue = contractsWithValue.reduce((sum, contract) => {
    const details = contract.contract_details;
    const match = details.match(/月額[^:]*:?\s*([0-9,]+)/);
    if (match) {
      const value = parseInt(match[1].replace(/,/g, ''));
      return sum + (isNaN(value) ? 0 : value);
    }
    return sum;
  }, 0);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#52c41a';
      case 'expiring': return '#faad14';
      case 'expired': return '#ff4d4f';
      default: return '#d9d9d9';
    }
  };

  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} lg={6}>
        <Card>
          <Statistic
            title="Total Contracts"
            value={totalContracts}
            prefix={<FileTextOutlined style={{ color: '#8B4513' }} />}
            valueStyle={{ color: '#2c3e50' }}
          />
        </Card>
      </Col>
      
      <Col xs={24} sm={12} lg={6}>
        <Card>
          <Statistic
            title="Active Contracts"
            value={activeContracts}
            prefix={<CheckCircleOutlined style={{ color: getStatusColor('active') }} />}
            valueStyle={{ color: getStatusColor('active') }}
          />
          <Progress 
            percent={totalContracts > 0 ? Math.round((activeContracts / totalContracts) * 100) : 0}
            size="small"
            strokeColor={getStatusColor('active')}
            style={{ marginTop: '8px' }}
          />
        </Card>
      </Col>
      
      <Col xs={24} sm={12} lg={6}>
        <Card>
          <Statistic
            title="Expiring Soon"
            value={expiringSoon}
            prefix={<ExclamationCircleOutlined style={{ color: getStatusColor('expiring') }} />}
            valueStyle={{ color: getStatusColor('expiring') }}
          />
          <Progress 
            percent={totalContracts > 0 ? Math.round((expiringSoon / totalContracts) * 100) : 0}
            size="small"
            strokeColor={getStatusColor('expiring')}
            style={{ marginTop: '8px' }}
          />
        </Card>
      </Col>
      
      <Col xs={24} sm={12} lg={6}>
        <Card>
          <Statistic
            title="Expired"
            value={expiredContracts}
            prefix={<WarningOutlined style={{ color: getStatusColor('expired') }} />}
            valueStyle={{ color: getStatusColor('expired') }}
          />
          <Progress 
            percent={totalContracts > 0 ? Math.round((expiredContracts / totalContracts) * 100) : 0}
            size="small"
            strokeColor={getStatusColor('expired')}
            style={{ marginTop: '8px' }}
          />
        </Card>
      </Col>
      
      {totalMonthlyValue > 0 && (
        <Col xs={24}>
          <Card>
            <div style={{ textAlign: 'center' }}>
              <Text strong style={{ fontSize: '16px', color: '#2c3e50' }}>
                Total Monthly Contract Value
              </Text>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#8B4513', marginTop: '8px' }}>
                ¥{totalMonthlyValue.toLocaleString()}
              </div>
              <Text type="secondary" style={{ fontSize: '12px' }}>
                Based on {contractsWithValue.length} contracts with value information
              </Text>
            </div>
          </Card>
        </Col>
      )}
    </Row>
  );
};

export default ContractStats;
