"""Azure Blob Storage service for file upload/download operations"""

import io
import uuid
from datetime import datetime, timedelta
from typing import Optional, Tuple
from azure.storage.blob import (
    BlobServiceClient,
    BlobClient,
    generate_blob_sas,
    BlobSasPermissions,
    ContentSettings,
)
from azure.core.exceptions import AzureError
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class AzureBlobService:
    """Service to handle Azure Blob Storage operations for contract files"""

    def __init__(self):
        try:
            self.blob_service_client = BlobServiceClient(
                account_url=settings.AZURE_SA_URL, credential=settings.AZURE_SA_KEY
            )
            self.container_name = settings.AZURE_CONTAINER_NAME
            self._ensure_container_exists()
        except Exception as e:
            logger.error(f"Failed to initialize Azure Blob Service: {e}")
            raise

    def _ensure_container_exists(self):
        """Ensure container exists, create if not present"""
        try:
            container_client = self.blob_service_client.get_container_client(
                self.container_name
            )
            if not container_client.exists():
                container_client.create_container()
                logger.info(f"Created container: {self.container_name}")
        except Exception as e:
            logger.error(f"Error ensuring container exists: {e}")
            raise

    def upload_file(
        self,
        file_data: bytes,
        filename: str,
        content_type: str = "application/octet-stream",
    ) -> Tuple[bool, str]:
        """
        Upload file to Azure Blob Storage

        Args:
            file_data: File data as bytes
            filename: File name
            content_type: MIME type of the file

        Returns:
            Tuple[bool, str]: (success, blob_url_or_error_message)
        """
        try:
            # Create unique blob name
            file_extension = filename.split(".")[-1] if "." in filename else ""
            blob_name = f"{datetime.utcnow().strftime('%Y/%m/%d')}/{uuid.uuid4()}.{file_extension}"

            # Upload file
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=blob_name
            )

            blob_client.upload_blob(
                file_data,
                blob_type="BlockBlob",
                content_settings=ContentSettings(content_type=content_type),
                overwrite=True,
            )

            # Return URL
            blob_url = blob_client.url
            logger.info(f"Successfully uploaded file: {blob_name}")

            return True, blob_url

        except AzureError as e:
            logger.error(f"Azure error uploading file: {e}")
            return False, f"Azure error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error uploading file: {e}")
            return False, f"Error: {str(e)}"

    def download_file(self, blob_url: str) -> Tuple[bool, Optional[bytes], str]:
        """
        Download file from Azure Blob Storage

        Args:
            blob_url: URL of the blob

        Returns:
            Tuple[bool, Optional[bytes], str]: (success, file_data, error_message)
        """
        try:
            # Extract blob name from URL
            blob_name = blob_url.split(f"/{self.container_name}/")[-1]

            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=blob_name
            )

            blob_data = blob_client.download_blob()
            file_data = blob_data.readall()

            logger.info(f"Successfully downloaded file: {blob_name}")
            return True, file_data, ""

        except AzureError as e:
            logger.error(f"Azure error downloading file: {e}")
            return False, None, f"Azure error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error downloading file: {e}")
            return False, None, f"Error: {str(e)}"

    def generate_download_url(
        self, blob_url: str, expiry_hours: int = 24
    ) -> Tuple[bool, Optional[str], str]:
        """
        Generate time-limited download URL

        Args:
            blob_url: URL of the blob
            expiry_hours: Number of hours until expiry

        Returns:
            Tuple[bool, Optional[str], str]: (success, signed_url, error_message)
        """
        try:
            # Extract blob name from URL
            blob_name = blob_url.split(f"/{self.container_name}/")[-1]

            # Generate SAS token
            expiry_time = datetime.utcnow() + timedelta(hours=expiry_hours)

            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=blob_name
            )

            sas_token = generate_blob_sas(
                account_name=blob_client.account_name,
                container_name=self.container_name,
                blob_name=blob_name,
                account_key=settings.AZURE_SA_KEY,
                permission=BlobSasPermissions(read=True),
                expiry=expiry_time,
            )

            signed_url = f"{blob_url}?{sas_token}"
            return True, signed_url, ""

        except Exception as e:
            logger.error(f"Error generating download URL: {e}")
            return False, None, f"Error: {str(e)}"

    def delete_file(self, blob_url: str) -> Tuple[bool, str]:
        """
        Delete file from Azure Blob Storage

        Args:
            blob_url: URL of the blob

        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            # Extract blob name from URL
            blob_name = blob_url.split(f"/{self.container_name}/")[-1]

            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=blob_name
            )

            blob_client.delete_blob()
            logger.info(f"Successfully deleted file: {blob_name}")

            return True, ""

        except AzureError as e:
            logger.error(f"Azure error deleting file: {e}")
            return False, f"Azure error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error deleting file: {e}")
            return False, f"Error: {str(e)}"

    def get_file_info(self, blob_url: str) -> Tuple[bool, Optional[dict], str]:
        """
        Get file information from Azure Blob Storage

        Args:
            blob_url: URL of the blob

        Returns:
            Tuple[bool, Optional[dict], str]: (success, file_info, error_message)
        """
        try:
            # Extract blob name from URL
            blob_name = blob_url.split(f"/{self.container_name}/")[-1]

            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=blob_name
            )

            properties = blob_client.get_blob_properties()

            file_info = {
                "name": blob_name,
                "size": properties.size,
                "content_type": properties.content_settings.content_type,
                "last_modified": properties.last_modified,
                "created": properties.creation_time,
                "url": blob_url,
            }

            return True, file_info, ""

        except AzureError as e:
            logger.error(f"Azure error getting file info: {e}")
            return False, None, f"Azure error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error getting file info: {e}")
            return False, None, f"Error: {str(e)}"


# Global service instance
azure_blob_service = AzureBlobService()
