import os
import logging
from azure.storage.blob import BlobServiceClient, ContentSettings
from typing import Optional, Tuple
import uuid
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)


class AzureStorageService:
    """Service for handling file uploads to Azure Blob Storage"""
    
    def __init__(self):
        self.storage_url = os.getenv("AZURE_SA_URL")
        self.storage_key = os.getenv("AZURE_SA_KEY")
        self.container_name = os.getenv("AZURE_CONTAINER_NAME")
        
        if not all([self.storage_url, self.storage_key, self.container_name]):
            raise ValueError("Azure Storage configuration is missing in environment variables")
        
        # Initialize blob service client
        self.blob_service_client = BlobServiceClient(
            account_url=self.storage_url,
            credential=self.storage_key
        )
        
        # Ensure container exists
        self._ensure_container_exists()
    
    def _ensure_container_exists(self):
        """Ensure the container exists, create if it doesn't"""
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            if not container_client.exists():
                container_client.create_container()
                logger.info(f"✅ Created container: {self.container_name}")
            else:
                logger.info(f"✅ Container already exists: {self.container_name}")
        except Exception as e:
            logger.error(f"❌ Error ensuring container exists: {str(e)}")
            raise
    
    def upload_file(
        self, 
        file_content: bytes, 
        file_name: str,
        content_type: str = "application/octet-stream",
        user_email: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Upload a file to Azure Blob Storage
        
        Args:
            file_content: Binary content of the file
            file_name: Original filename
            content_type: MIME type of the file
            user_email: Email of the user uploading the file
            
        Returns:
            Tuple of (success: bool, message: str, blob_url: Optional[str])
        """
        try:
            # Generate unique blob name with timestamp and UUID
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(file_name)[1]
            unique_id = str(uuid.uuid4())[:8]
            
            # Create blob name with user email prefix if provided
            if user_email:
                safe_email = user_email.replace("@", "_at_").replace(".", "_")
                blob_name = f"{safe_email}/{timestamp}_{unique_id}{file_extension}"
            else:
                blob_name = f"{timestamp}_{unique_id}{file_extension}"
            
            # Get blob client
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            # Upload the file
            blob_client.upload_blob(
                file_content,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type)
            )
            
            # Get the blob URL
            blob_url = blob_client.url
            
            logger.info(f"✅ File uploaded successfully: {blob_name}")
            return True, "File uploaded successfully", blob_url
            
        except Exception as e:
            logger.error(f"❌ Error uploading file to Azure Storage: {str(e)}")
            return False, f"Failed to upload file: {str(e)}", None
    
    def download_file(self, blob_name: str) -> Tuple[bool, str, Optional[bytes]]:
        """
        Download a file from Azure Blob Storage
        
        Args:
            blob_name: Name of the blob to download
            
        Returns:
            Tuple of (success: bool, message: str, file_content: Optional[bytes])
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            file_content = blob_client.download_blob().readall()
            
            logger.info(f"✅ File downloaded successfully: {blob_name}")
            return True, "File downloaded successfully", file_content
            
        except Exception as e:
            logger.error(f"❌ Error downloading file from Azure Storage: {str(e)}")
            return False, f"Failed to download file: {str(e)}", None
    
    def delete_file(self, blob_name: str) -> Tuple[bool, str]:
        """
        Delete a file from Azure Blob Storage
        
        Args:
            blob_name: Name of the blob to delete
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            blob_client.delete_blob()
            
            logger.info(f"✅ File deleted successfully: {blob_name}")
            return True, "File deleted successfully"
            
        except Exception as e:
            logger.error(f"❌ Error deleting file from Azure Storage: {str(e)}")
            return False, f"Failed to delete file: {str(e)}"


# Global instance
storage_service = AzureStorageService()

