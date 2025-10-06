import React, { useState } from 'react';
import { Modal, Upload, message, Progress, Typography, Alert, Divider } from 'antd';
import { InboxOutlined, FileTextOutlined, CheckCircleOutlined, LoadingOutlined } from '@ant-design/icons';

const { Dragger } = Upload;
const { Text, Paragraph } = Typography;

const ContractUpload = ({ visible, onClose, onSuccess, userEmail }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStage, setUploadStage] = useState('idle'); // idle, uploading, extracting, saving, complete
  const [extractedData, setExtractedData] = useState(null);
  const [fileList, setFileList] = useState([]);

  const getStageMessage = () => {
    switch (uploadStage) {
      case 'uploading':
        return '☁️ Uploading file to Azure Storage...';
      case 'extracting':
        return '🤖 Extracting contract information using AI...';
      case 'saving':
        return '💾 Saving contract to database...';
      case 'complete':
        return '✅ Contract uploaded and saved successfully!';
      default:
        return '';
    }
  };

  const handleUpload = async (file) => {
    try {
      setUploading(true);
      setUploadProgress(0);
      setExtractedData(null);

      // Validate file type
      const allowedTypes = [
        'application/pdf',
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/gif',
        'image/webp'
      ];
      
      if (!allowedTypes.includes(file.type)) {
        message.error('Unsupported file type. Please upload PDF or image files (JPG, PNG, GIF, WEBP).');
        setUploading(false);
        return false;
      }

      // Check file size (max 10MB)
      const maxSize = 10 * 1024 * 1024; // 10MB
      if (file.size > maxSize) {
        message.error('File size exceeds 10MB limit.');
        setUploading(false);
        return false;
      }

      // Stage 1: Start upload
      setUploadStage('uploading');
      setUploadProgress(10);

      // Create FormData
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_email', userEmail);

      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 500);

      // Stage 2: Extracting
      setTimeout(() => {
        setUploadStage('extracting');
      }, 1000);

      // Upload to backend
      const response = await fetch('http://localhost:8000/api/v1/contracts/upload', {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      // Stage 3: Saving
      setUploadStage('saving');
      setUploadProgress(95);

      const result = await response.json();

      // Stage 4: Complete
      setUploadStage('complete');
      setUploadProgress(100);
      setExtractedData(result.extracted_data);

      message.success('Contract uploaded and extracted successfully!');

      // Wait a bit to show the success message, then close and refresh
      setTimeout(() => {
        onSuccess(result);
        handleClose();
      }, 2000);

      return false; // Prevent default upload behavior

    } catch (error) {
      console.error('Upload error:', error);
      message.error(`Upload failed: ${error.message}`);
      setUploading(false);
      setUploadStage('idle');
      setUploadProgress(0);
      return false;
    }
  };

  const handleClose = () => {
    setFileList([]);
    setUploading(false);
    setUploadProgress(0);
    setUploadStage('idle');
    setExtractedData(null);
    onClose();
  };

  const uploadProps = {
    name: 'file',
    multiple: false,
    fileList: fileList,
    beforeUpload: (file) => {
      setFileList([file]);
      handleUpload(file);
      return false; // Prevent default upload
    },
    onRemove: () => {
      setFileList([]);
    },
    disabled: uploading,
    accept: '.pdf,.jpg,.jpeg,.png,.gif,.webp',
  };

  return (
    <Modal
      title="Upload Contract File"
      open={visible}
      onCancel={handleClose}
      footer={null}
      width={700}
      closable={!uploading}
      maskClosable={!uploading}
    >
      <Paragraph style={{ marginBottom: 16, color: '#666' }}>
        Upload a contract file (PDF or image) to automatically extract information using AI.
      </Paragraph>

      <Alert
        message="Supported Files"
        description="PDF, JPG, JPEG, PNG, GIF, WEBP (Max 10MB)"
        type="info"
        showIcon
        style={{ marginBottom: 16 }}
      />

      <Dragger {...uploadProps}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">Click or drag file to this area to upload</p>
        <p className="ant-upload-hint">
          Support for PDF and image files. The AI will automatically extract contract information.
        </p>
      </Dragger>

      {uploading && (
        <div style={{ marginTop: 24 }}>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: 12 }}>
            <LoadingOutlined style={{ fontSize: 20, marginRight: 12, color: '#1890ff' }} />
            <Text strong>{getStageMessage()}</Text>
          </div>
          <Progress percent={uploadProgress} status="active" />
          
          <div style={{ marginTop: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
              {uploadStage === 'uploading' && <LoadingOutlined style={{ marginRight: 8 }} />}
              {uploadStage !== 'uploading' && uploadStage !== 'idle' && <CheckCircleOutlined style={{ marginRight: 8, color: '#52c41a' }} />}
              <Text type={uploadStage === 'uploading' ? 'default' : 'secondary'}>
                Step 1: Upload to Azure Storage
              </Text>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
              {uploadStage === 'extracting' && <LoadingOutlined style={{ marginRight: 8 }} />}
              {['saving', 'complete'].includes(uploadStage) && <CheckCircleOutlined style={{ marginRight: 8, color: '#52c41a' }} />}
              <Text type={uploadStage === 'extracting' ? 'default' : 'secondary'}>
                Step 2: AI Information Extraction
              </Text>
            </div>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              {uploadStage === 'saving' && <LoadingOutlined style={{ marginRight: 8 }} />}
              {uploadStage === 'complete' && <CheckCircleOutlined style={{ marginRight: 8, color: '#52c41a' }} />}
              <Text type={['saving', 'complete'].includes(uploadStage) ? 'default' : 'secondary'}>
                Step 3: Save to Database
              </Text>
            </div>
          </div>
        </div>
      )}

      {extractedData && uploadStage === 'complete' && (
        <div style={{ marginTop: 24 }}>
          <Divider>Extracted Information</Divider>
          <div style={{ 
            background: '#f5f5f5', 
            padding: 16, 
            borderRadius: 8,
            maxHeight: 300,
            overflowY: 'auto'
          }}>
            {extractedData.service_name && (
              <div style={{ marginBottom: 8 }}>
                <Text strong>Service Name: </Text>
                <Text>{extractedData.service_name}</Text>
              </div>
            )}
            {extractedData.supplier_name && (
              <div style={{ marginBottom: 8 }}>
                <Text strong>Supplier: </Text>
                <Text>{extractedData.supplier_name}</Text>
              </div>
            )}
            {extractedData.customer_name && (
              <div style={{ marginBottom: 8 }}>
                <Text strong>Customer: </Text>
                <Text>{extractedData.customer_name}</Text>
              </div>
            )}
            {extractedData.contract_start_date && (
              <div style={{ marginBottom: 8 }}>
                <Text strong>Start Date: </Text>
                <Text>{extractedData.contract_start_date}</Text>
              </div>
            )}
            {extractedData.contract_end_date && (
              <div style={{ marginBottom: 8 }}>
                <Text strong>End Date: </Text>
                <Text>{extractedData.contract_end_date}</Text>
              </div>
            )}
            {extractedData.termination_notice_period && (
              <div style={{ marginBottom: 8 }}>
                <Text strong>Notice Period: </Text>
                <Text>{extractedData.termination_notice_period}</Text>
              </div>
            )}
            {extractedData.contract_details && (
              <div style={{ marginBottom: 8 }}>
                <Text strong>Details: </Text>
                <Text>{extractedData.contract_details}</Text>
              </div>
            )}
          </div>
        </div>
      )}
    </Modal>
  );
};

export default ContractUpload;

