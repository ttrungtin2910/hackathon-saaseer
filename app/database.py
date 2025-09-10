from azure.cosmos import CosmosClient, PartitionKey, exceptions
from typing import Optional, List, Dict, Any
from app.models import ContractData, ContractUpdateData
from config.settings import get_settings
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable Azure Cosmos DB verbose logging
azure_logger = logging.getLogger('azure.core.pipeline.policies.http_logging_policy')
azure_logger.setLevel(logging.WARNING)

azure_cosmos_logger = logging.getLogger('azure.cosmos')
azure_cosmos_logger.setLevel(logging.WARNING)

# Get settings
settings = get_settings()


class CosmosDBManager:
    """
    Azure Cosmos DB manager for contract data operations
    """
    
    def __init__(self):
        # Get configuration from settings
        self.endpoint = settings.cosmos_endpoint
        self.key = settings.cosmos_key
        self.database_name = settings.cosmos_database_name
        self.container_name = settings.cosmos_container_name
        
        # Initialize Cosmos client
        try:
            self.client = CosmosClient(self.endpoint, self.key)
            self.database = self.client.get_database_client(self.database_name)
            self.container = self.database.get_container_client(self.container_name)
            logger.info(f"✅ Connected to Azure Cosmos DB: {self.database_name}/{self.container_name}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Cosmos DB: {str(e)}")
            raise
    
    async def create_database_and_container_if_not_exists(self):
        """
        Create database and container if they don't exist
        """
        try:
            # Create database if it doesn't exist
            try:
                # For serverless accounts, don't specify offer_throughput
                database = self.client.create_database(
                    id=self.database_name
                )
                logger.info(f"📁 Created database: {self.database_name}")
            except exceptions.CosmosResourceExistsError:
                database = self.client.get_database_client(self.database_name)
                logger.info(f"📁 Database {self.database_name} already exists")
            except Exception as e:
                if "serverless" in str(e).lower():
                    logger.warning(f"⚠️ Serverless account detected, using existing database: {self.database_name}")
                    database = self.client.get_database_client(self.database_name)
                else:
                    raise
            
            # Create container if it doesn't exist
            try:
                # For serverless accounts, don't specify offer_throughput
                container = database.create_container(
                    id=self.container_name,
                    partition_key=PartitionKey(path="/UserEmail")
                )
                logger.info(f"📦 Created container: {self.container_name}")
            except exceptions.CosmosResourceExistsError:
                container = database.get_container_client(self.container_name)
                logger.info(f"📦 Container {self.container_name} already exists")
            except Exception as e:
                if "serverless" in str(e).lower():
                    logger.warning(f"⚠️ Serverless account detected, using existing container: {self.container_name}")
                    container = database.get_container_client(self.container_name)
                else:
                    raise
                
            return True
        except Exception as e:
            logger.error(f"Error creating database/container: {str(e)}")
            return False
    
    async def create_contract(self, contract_data: ContractData) -> Dict[str, Any]:
        """
        Create a new contract in Cosmos DB
        """
        try:
            # Convert Pydantic model to dict
            contract_dict = contract_data.dict()
            
            # Ensure created_at and updated_at are ISO format strings
            if contract_dict.get('created_at'):
                contract_dict['created_at'] = contract_dict['created_at'].isoformat()
            if contract_dict.get('updated_at'):
                contract_dict['updated_at'] = contract_dict['updated_at'].isoformat()
            
            # Create item in Cosmos DB
            created_item = self.container.create_item(body=contract_dict)
            logger.info(f"✅ Contract created successfully: {contract_data.id}")
            
            return {
                "success": True,
                "message": "Contract created successfully",
                "data": created_item
            }
        except exceptions.CosmosResourceExistsError:
            logger.warning(f"⚠️ Contract already exists: {contract_data.id}")
            return {
                "success": False,
                "message": f"Contract with ID {contract_data.id} already exists"
            }
        except Exception as e:
            logger.error(f"❌ Error creating contract: {str(e)}")
            return {
                "success": False,
                "message": f"Error creating contract: {str(e)}"
            }
    
    async def get_contract(self, contract_id: str, user_email: str) -> Dict[str, Any]:
        """
        Retrieve a contract by ID and user email (partition key)
        """
        try:
            item = self.container.read_item(
                item=contract_id,
                partition_key=user_email
            )
            logger.info(f"Retrieved contract with ID: {contract_id}")
            
            return {
                "success": True,
                "message": "Contract retrieved successfully",
                "data": item
            }
        except exceptions.CosmosResourceNotFoundError:
            logger.warning(f"Contract with ID {contract_id} not found")
            return {
                "success": False,
                "message": f"Contract with ID {contract_id} not found"
            }
        except Exception as e:
            logger.error(f"Error retrieving contract: {str(e)}")
            return {
                "success": False,
                "message": f"Error retrieving contract: {str(e)}"
            }
    
    async def update_contract(self, contract_id: str, user_email: str, update_data: ContractUpdateData) -> Dict[str, Any]:
        """
        Update an existing contract
        """
        try:
            # First, get the existing contract
            existing_result = await self.get_contract(contract_id, user_email)
            if not existing_result["success"]:
                return existing_result
            
            existing_contract = existing_result["data"]
            
            # Update only the fields that are provided
            update_dict = update_data.dict(exclude_unset=True)
            
            # Ensure updated_at is set to current time
            update_dict['updated_at'] = datetime.utcnow().isoformat()
            
            # Merge with existing data
            for key, value in update_dict.items():
                if value is not None:
                    existing_contract[key] = value
            
            # Update in Cosmos DB
            updated_item = self.container.replace_item(
                item=contract_id,
                body=existing_contract
            )
            logger.info(f"Updated contract with ID: {contract_id}")
            
            return {
                "success": True,
                "message": "Contract updated successfully",
                "data": updated_item
            }
        except Exception as e:
            logger.error(f"Error updating contract: {str(e)}")
            return {
                "success": False,
                "message": f"Error updating contract: {str(e)}"
            }
    
    async def delete_contract(self, contract_id: str, user_email: str) -> Dict[str, Any]:
        """
        Delete a contract by ID and user email
        """
        try:
            self.container.delete_item(
                item=contract_id,
                partition_key=user_email
            )
            logger.info(f"Deleted contract with ID: {contract_id}")
            
            return {
                "success": True,
                "message": "Contract deleted successfully"
            }
        except exceptions.CosmosResourceNotFoundError:
            logger.warning(f"Contract with ID {contract_id} not found")
            return {
                "success": False,
                "message": f"Contract with ID {contract_id} not found"
            }
        except Exception as e:
            logger.error(f"Error deleting contract: {str(e)}")
            return {
                "success": False,
                "message": f"Error deleting contract: {str(e)}"
            }
    
    async def list_contracts_by_user(self, user_email: str, limit: int = 100) -> Dict[str, Any]:
        """
        List all contracts for a specific user
        """
        try:
            query = "SELECT * FROM c WHERE c.UserEmail = @user_email"
            parameters = [{"name": "@user_email", "value": user_email}]
            
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                max_item_count=limit,
                enable_cross_partition_query=False
            ))
            
            logger.info(f"Retrieved {len(items)} contracts for user: {user_email}")
            
            return {
                "success": True,
                "message": f"Retrieved {len(items)} contracts",
                "data": items,
                "count": len(items)
            }
        except Exception as e:
            logger.error(f"Error listing contracts: {str(e)}")
            return {
                "success": False,
                "message": f"Error listing contracts: {str(e)}"
            }


# Global instance
cosmos_db = CosmosDBManager()
