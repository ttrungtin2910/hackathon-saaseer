import React, { useState } from 'react';
import { Modal, Upload, message, Progress, Typography, Alert, Divider, Button, Space, List, Card } from 'antd';
import { InboxOutlined, FileTextOutlined, CheckCircleOutlined, LoadingOutlined, DeleteOutlined, UploadOutlined } from '@ant-design/icons';

const { Dragger } = Upload;
const { Text, Paragraph } = Typography;

const ContractUpload = ({ visible, onClose, onSuccess, userEmail }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStage, setUploadStage] = useState('idle'); // idle, uploading, extracting, saving, complete
  const [extractedData, setExtractedData] = useState(null);
  const [fileList, setFileList] = useState([]);
  const [uploadResults, setUploadResults] = useState([]);
  const [currentFileIndex, setCurrentFileIndex] = useState(0);
  const [totalFiles, setTotalFiles] = useState(0);

  const getStageMessage = () => {
    switch (uploadStage) {
      case 'uploading':
        return `☁️ Uploading file ${currentFileIndex + 1} of ${totalFiles} to Azure Storage...`;
      case 'extracting':
        return `🤖 Extracting contract information from file ${currentFileIndex + 1} of ${totalFiles}...`;
      case 'saving':
        return `💾 Saving contract ${currentFileIndex + 1} of ${totalFiles} to database...`;
      case 'complete':
        return `✅ All ${totalFiles} contracts uploaded and saved successfully!`;
      default:
        return '';
    }
  };

  const uploadSingleFile = async (file, fileIndex) => {
    try {
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
        throw new Error(`Unsupported file type: ${file.name}`);
      }

      // Check file size (max 10MB)
      const maxSize = 10 * 1024 * 1024; // 10MB
      if (file.size > maxSize) {
        throw new Error(`File size exceeds 10MB limit: ${file.name}`);
      }

      // Create FormData
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_email', userEmail);

      // Upload to backend
      const response = await fetch('http://localhost:8000/api/v1/contracts/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const result = await response.json();
      return { success: true, data: result, fileName: file.name };

    } catch (error) {
      return { success: false, error: error.message, fileName: file.name };
    }
  };

  const handleUploadAll = async () => {
    if (fileList.length === 0) {
      message.warning('Please select files to upload');
      return;
    }

    setUploading(true);
    setUploadResults([]);
    setUploadProgress(0);
    setTotalFiles(fileList.length);
    setCurrentFileIndex(0);

    const results = [];

    for (let i = 0; i < fileList.length; i++) {
      setCurrentFileIndex(i);
      
      // Stage 1: Uploading
      setUploadStage('uploading');
      setUploadProgress((i / fileList.length) * 100);
      
      // Stage 2: Extracting
      setTimeout(() => {
        setUploadStage('extracting');
      }, 500);
      
      // Stage 3: Saving
      setTimeout(() => {
        setUploadStage('saving');
      }, 1000);

      const result = await uploadSingleFile(fileList[i], i);
      results.push(result);

      // Update progress
      setUploadProgress(((i + 1) / fileList.length) * 100);
      
      // Small delay between files
      if (i < fileList.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 500));
      }
    }

    // Complete
    setUploadStage('complete');
    setUploadResults(results);
    
    const successCount = results.filter(r => r.success).length;
    const failCount = results.filter(r => !r.success).length;

    if (successCount > 0) {
      message.success(`${successCount} contract(s) uploaded successfully!`);
      onSuccess({ successCount, results });
    }
    
    if (failCount > 0) {
      message.error(`${failCount} file(s) failed to upload`);
    }

    // Auto close after 3 seconds if all successful
    if (failCount === 0) {
      setTimeout(() => {
        handleClose();
      }, 3000);
    }
  };

  const handleClose = () => {
    setFileList([]);
    setUploading(false);
    setUploadProgress(0);
    setUploadStage('idle');
    setExtractedData(null);
    setUploadResults([]);
    setCurrentFileIndex(0);
    setTotalFiles(0);
    onClose();
  };

  const uploadProps = {
    name: 'file',
    multiple: true,
    fileList: fileList,
    beforeUpload: (file) => {
      // Add file to list but don't upload immediately
      setFileList(prev => [...prev, file]);
      return false; // Prevent default upload
    },
    onRemove: (file) => {
      setFileList(prev => prev.filter(f => f.uid !== file.uid));
    },
    disabled: uploading,
    accept: '.pdf,.jpg,.jpeg,.png,.gif,.webp',
    showUploadList: {
      showPreviewIcon: false,
      showRemoveIcon: true,
    },
  };

  return (
    <Modal
      title="Upload Contract Files"
      open={visible}
      onCancel={handleClose}
      footer={null}
      width={800}
      closable={!uploading}
      maskClosable={!uploading}
    >
      <Paragraph style={{ marginBottom: 16, color: '#666' }}>
        Upload multiple contract files (PDF or images) to automatically extract information using AI.
      </Paragraph>

      <Alert
        message="Supported Files"
        description="PDF, JPG, JPEG, PNG, GIF, WEBP (Max 10MB each)"
        type="info"
        showIcon
        style={{ marginBottom: 16 }}
      />

      <Dragger {...uploadProps}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">Click or drag files to this area to upload</p>
        <p className="ant-upload-hint">
          Support for multiple PDF and image files. The AI will automatically extract contract information from each file.
        </p>
      </Dragger>

      {fileList.length > 0 && !uploading && (
        <div style={{ marginTop: 16 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <Text strong>Selected Files ({fileList.length})</Text>
            <Button 
              type="primary" 
              icon={<UploadOutlined />}
              onClick={handleUploadAll}
              disabled={uploading}
            >
              Upload All Files
            </Button>
          </div>
          <List
            size="small"
            dataSource={fileList}
            renderItem={(file) => (
              <List.Item>
                <Space>
                  <FileTextOutlined />
                  <Text>{file.name}</Text>
                  <Text type="secondary">({(file.size / 1024 / 1024).toFixed(2)} MB)</Text>
                </Space>
              </List.Item>
            )}
          />
        </div>
      )}

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

      {uploadResults.length > 0 && uploadStage === 'complete' && (
        <div style={{ marginTop: 24 }}>
          <Divider>Upload Results</Divider>
          <div style={{ 
            maxHeight: 400,
            overflowY: 'auto'
          }}>
            {uploadResults.map((result, index) => (
              <Card 
                key={index}
                size="small" 
                style={{ marginBottom: 12 }}
                title={
                  <Space>
                    {result.success ? (
                      <CheckCircleOutlined style={{ color: '#52c41a' }} />
                    ) : (
                      <DeleteOutlined style={{ color: '#ff4d4f' }} />
                    )}
                    <Text>{result.fileName}</Text>
                  </Space>
                }
              >
                {result.success ? (
                  <div>
                    {result.data.extracted_data.service_name && (
                      <div style={{ marginBottom: 4 }}>
                        <Text strong>Service: </Text>
                        <Text>{result.data.extracted_data.service_name}</Text>
                      </div>
                    )}
                    {result.data.extracted_data.supplier_name && (
                      <div style={{ marginBottom: 4 }}>
                        <Text strong>Supplier: </Text>
                        <Text>{result.data.extracted_data.supplier_name}</Text>
                      </div>
                    )}
                    {result.data.extracted_data.customer_name && (
                      <div style={{ marginBottom: 4 }}>
                        <Text strong>Customer: </Text>
                        <Text>{result.data.extracted_data.customer_name}</Text>
                      </div>
                    )}
                    <Text type="success">✅ Extracted successfully</Text>
                  </div>
                ) : (
                  <Text type="danger">❌ {result.error}</Text>
                )}
              </Card>
            ))}
          </div>
          
          {uploadResults.filter(r => r.success).length > 0 && (
            <div style={{ marginTop: 16, textAlign: 'center' }}>
              <Button type="primary" onClick={handleClose}>
                Close
              </Button>
            </div>
          )}
        </div>
      )}
    </Modal>
  );
};

export default ContractUpload;

