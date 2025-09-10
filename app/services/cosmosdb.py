"""CosmosDB service for contract and user requirement data operations"""

from typing import List, Optional, Dict, Any
from azure.cosmos import CosmosClient, exceptions
from azure.cosmos.database import DatabaseProxy
from azure.cosmos.container import ContainerProxy
import logging
from datetime import datetime

from app.models.contract import ContractInformation, UserRequirement
from app.config import settings

logger = logging.getLogger(__name__)


class CosmosDBService:
    """Service to handle CosmosDB operations for contract management"""

    def __init__(self):
        self.client = None
        self.database = None
        self.contracts_container = None
        self.requirements_container = None
        self.is_connected = False

        try:
            self.client = CosmosClient(settings.COSMOS_ENDPOINT, settings.COSMOS_KEY)
            self.database_name = settings.COSMOS_DATABASE_NAME
            self.database = self._get_or_create_database()

            # Container names
            self.contracts_container_name = "ContractInformation"
            self.requirements_container_name = "UserRequirement"

            # Initialize containers
            self.contracts_container = self._get_or_create_container(
                self.contracts_container_name
            )
            self.requirements_container = self._get_or_create_container(
                self.requirements_container_name
            )

            self.is_connected = True
            logger.info("CosmosDB service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize CosmosDB service: {e}")
            logger.warning(
                "CosmosDB service will be unavailable. App will continue with limited functionality."
            )
            self.is_connected = False

    def _get_or_create_database(self) -> DatabaseProxy:
        """Get or create database"""
        try:
            database = self.client.create_database_if_not_exists(id=self.database_name)
            logger.info(f"Database '{self.database_name}' ready")
            return database
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error creating/getting database: {e}")
            raise

    def _get_or_create_container(self, container_name: str) -> ContainerProxy:
        """Get or create container"""
        try:
            container = self.database.create_container_if_not_exists(
                id=container_name, partition_key="/id", offer_throughput=400
            )
            logger.info(f"Container '{container_name}' ready")
            return container
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error creating/getting container {container_name}: {e}")
            raise

    # Contract Information operations
    def insert_contract(self, contract: ContractInformation) -> bool:
        """Insert new contract into CosmosDB"""
        if not self.is_connected:
            logger.error("CosmosDB not connected - cannot insert contract")
            return False

        try:
            contract_dict = contract.dict()
            # Convert ALL datetime objects to ISO format strings
            datetime_fields = ["CreatedAt", "UpdatedAt", "StartDate", "EndDate"]
            for field in datetime_fields:
                if isinstance(contract_dict.get(field), datetime):
                    contract_dict[field] = contract_dict[field].isoformat()

            # Ensure UpdatedAt is always set
            if not contract_dict.get("UpdatedAt"):
                contract_dict["UpdatedAt"] = datetime.utcnow().isoformat()

            self.contracts_container.create_item(body=contract_dict)
            logger.info(f"Successfully inserted contract: {contract.ContractID}")
            return True

        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error inserting contract: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error inserting contract: {e}")
            return False

    def get_contracts_by_username(self, username: str) -> List[ContractInformation]:
        """Get contracts by UserName"""
        if not self.is_connected:
            logger.error("CosmosDB not connected - cannot get contracts")
            return []

        try:
            query = (
                "SELECT * FROM c WHERE c.UserName = @username ORDER BY c.CreatedAt DESC"
            )
            parameters = [{"name": "@username", "value": username}]

            items = list(
                self.contracts_container.query_items(
                    query=query,
                    parameters=parameters,
                    enable_cross_partition_query=True,
                )
            )

            contracts = []
            for item in items:
                try:
                    # Convert datetime strings back to datetime objects
                    if "CreatedAt" in item and isinstance(item["CreatedAt"], str):
                        item["CreatedAt"] = datetime.fromisoformat(
                            item["CreatedAt"].replace("Z", "+00:00")
                        )
                    if "UpdatedAt" in item and isinstance(item["UpdatedAt"], str):
                        item["UpdatedAt"] = datetime.fromisoformat(
                            item["UpdatedAt"].replace("Z", "+00:00")
                        )
                    if "StartDate" in item and isinstance(item["StartDate"], str):
                        item["StartDate"] = datetime.fromisoformat(
                            item["StartDate"].replace("Z", "+00:00")
                        )
                    if "EndDate" in item and isinstance(item["EndDate"], str):
                        item["EndDate"] = datetime.fromisoformat(
                            item["EndDate"].replace("Z", "+00:00")
                        )

                    contract = ContractInformation(**item)
                    contracts.append(contract)
                except Exception as e:
                    logger.warning(f"Error parsing contract item: {e}")
                    continue

            logger.info(f"Found {len(contracts)} contracts for user: {username}")
            return contracts

        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error querying contracts by username: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error querying contracts: {e}")
            return []

    def get_contract_by_id(self, contract_id: str) -> Optional[ContractInformation]:
        """Get contract by ContractID"""
        try:
            query = "SELECT * FROM c WHERE c.ContractID = @contract_id"
            parameters = [{"name": "@contract_id", "value": contract_id}]

            items = list(
                self.contracts_container.query_items(
                    query=query,
                    parameters=parameters,
                    enable_cross_partition_query=True,
                )
            )

            if not items:
                return None

            item = items[0]

            # Convert datetime strings back to datetime objects
            if "CreatedAt" in item and isinstance(item["CreatedAt"], str):
                item["CreatedAt"] = datetime.fromisoformat(
                    item["CreatedAt"].replace("Z", "+00:00")
                )
            if "UpdatedAt" in item and isinstance(item["UpdatedAt"], str):
                item["UpdatedAt"] = datetime.fromisoformat(
                    item["UpdatedAt"].replace("Z", "+00:00")
                )
            if "StartDate" in item and isinstance(item["StartDate"], str):
                item["StartDate"] = datetime.fromisoformat(
                    item["StartDate"].replace("Z", "+00:00")
                )
            if "EndDate" in item and isinstance(item["EndDate"], str):
                item["EndDate"] = datetime.fromisoformat(
                    item["EndDate"].replace("Z", "+00:00")
                )

            contract = ContractInformation(**item)
            logger.info(f"Found contract: {contract_id}")
            return contract

        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error getting contract by ID: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting contract: {e}")
            return None

    def update_contract(self, contract: ContractInformation) -> bool:
        """Update contract information"""
        try:
            contract_dict = contract.dict()
            # Convert ALL datetime objects to ISO format strings
            datetime_fields = ["CreatedAt", "UpdatedAt", "StartDate", "EndDate"]
            for field in datetime_fields:
                if isinstance(contract_dict.get(field), datetime):
                    contract_dict[field] = contract_dict[field].isoformat()

            # Ensure UpdatedAt is always set
            contract_dict["UpdatedAt"] = datetime.utcnow().isoformat()

            self.contracts_container.replace_item(item=contract.id, body=contract_dict)
            logger.info(f"Successfully updated contract: {contract.ContractID}")
            return True

        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error updating contract: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error updating contract: {e}")
            return False

    # User Requirement operations
    def insert_user_requirement(self, requirement: UserRequirement) -> bool:
        """Insert new user requirement"""
        if not self.is_connected:
            logger.error("CosmosDB not connected - cannot insert user requirement")
            return False

        try:
            requirement_dict = requirement.dict()
            # Convert datetime objects to ISO format strings
            if isinstance(requirement_dict.get("CreatedAt"), datetime):
                requirement_dict["CreatedAt"] = requirement_dict[
                    "CreatedAt"
                ].isoformat()

            self.requirements_container.create_item(body=requirement_dict)
            logger.info(
                f"Successfully inserted user requirement: {requirement.UserRequirementID}"
            )
            return True

        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error inserting user requirement: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error inserting user requirement: {e}")
            return False

    def get_requirements_by_contract_id(
        self, contract_id: str
    ) -> List[UserRequirement]:
        """Get requirements by ContractID"""
        try:
            query = "SELECT * FROM c WHERE c.ContractID = @contract_id ORDER BY c.CreatedAt DESC"
            parameters = [{"name": "@contract_id", "value": contract_id}]

            items = list(
                self.requirements_container.query_items(
                    query=query,
                    parameters=parameters,
                    enable_cross_partition_query=True,
                )
            )

            requirements = []
            for item in items:
                try:
                    # Convert datetime strings back to datetime objects
                    if "CreatedAt" in item and isinstance(item["CreatedAt"], str):
                        item["CreatedAt"] = datetime.fromisoformat(
                            item["CreatedAt"].replace("Z", "+00:00")
                        )

                    requirement = UserRequirement(**item)
                    requirements.append(requirement)
                except Exception as e:
                    logger.warning(f"Error parsing requirement item: {e}")
                    continue

            logger.info(
                f"Found {len(requirements)} requirements for contract: {contract_id}"
            )
            return requirements

        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error querying requirements by contract ID: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error querying requirements: {e}")
            return []

    def get_requirement_by_id(self, requirement_id: str) -> Optional[UserRequirement]:
        """Get requirement by UserRequirementID"""
        try:
            query = "SELECT * FROM c WHERE c.UserRequirementID = @requirement_id"
            parameters = [{"name": "@requirement_id", "value": requirement_id}]

            items = list(
                self.requirements_container.query_items(
                    query=query,
                    parameters=parameters,
                    enable_cross_partition_query=True,
                )
            )

            if not items:
                return None

            item = items[0]

            # Convert datetime strings back to datetime objects
            if "CreatedAt" in item and isinstance(item["CreatedAt"], str):
                item["CreatedAt"] = datetime.fromisoformat(
                    item["CreatedAt"].replace("Z", "+00:00")
                )

            requirement = UserRequirement(**item)
            logger.info(f"Found requirement: {requirement_id}")
            return requirement

        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error getting requirement by ID: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting requirement: {e}")
            return None


# Global service instance
cosmosdb_service = CosmosDBService()
