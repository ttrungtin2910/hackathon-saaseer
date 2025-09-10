"""Contract and User Requirement data models"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid


class ContractInformation(BaseModel):
    """Model for ContractInformation table in CosmosDB"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # CosmosDB document id
    ContractID: str = Field(default_factory=lambda: str(uuid.uuid4()))
    UserName: str
    ContractFilePath: str  # Link to Azure Blob
    StartDate: Optional[datetime] = None
    EndDate: Optional[datetime] = None
    Provider: Optional[str] = None
    Service: Optional[str] = None
    RenewalStatus: Optional[str] = None
    SummaryContract: Optional[str] = None
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class UserRequirement(BaseModel):
    """Model for UserRequirement table in CosmosDB"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # CosmosDB document id
    UserRequirementID: str = Field(default_factory=lambda: str(uuid.uuid4()))
    UserRequirementContent: str
    ContractID: str  # Foreign key reference
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


# Request/Response models for API
class ContractUploadRequest(BaseModel):
    """Request model for contract upload"""

    UserName: str


class ContractListResponse(BaseModel):
    """Response model for listing contracts"""

    contracts: List[ContractInformation]
    total: int


class ContractSearchRequest(BaseModel):
    """Request model for contract search"""

    UserName: str
    ContractID: str
    UserRequirementContent: str


class ContractSearchResponse(BaseModel):
    """Response model for contract search"""

    success: bool
    report: str
    user_requirement_id: str
    similar_services: List[dict] = []


class ContractInsertResponse(BaseModel):
    """Response model for contract insertion"""

    success: bool
    contract_id: str
    message: str
    extracted_data: Optional[dict] = None


# Models for extracted contract data from LangGraph
class ExtractedContractData(BaseModel):
    """Model for data extracted from contract analysis"""

    StartDate: Optional[str] = None
    EndDate: Optional[str] = None
    Provider: Optional[str] = None
    Service: Optional[str] = None
    RenewalStatus: Optional[str] = None
    Price: Optional[str] = None  # Giá tiền/phí dịch vụ
    Currency: Optional[str] = None  # Đơn vị tiền tệ
    SummaryContract: Optional[str] = None  # Tóm lược nội dung hợp đồng

    class Config:
        extra = "allow"  # Allow additional fields



