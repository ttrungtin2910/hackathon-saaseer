from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ContractData(BaseModel):
    """
    Contract data model for storing contract information in Azure Cosmos DB
    """
    id: str = Field(..., description="Unique identifier for the contract")
    contract_details: Optional[str] = Field(None, description="Contract details including location, area, monthly amount, and payment info")
    contract_end_date: Optional[str] = Field(None, description="Contract end date in YYYY/MM/DD format")
    contract_start_date: Optional[str] = Field(None, description="Contract start date in YYYY/MM/DD format")
    customer_name: Optional[str] = Field(None, description="Customer company name")
    LinkImage: Optional[str] = Field(None, description="Link to contract image/document")
    service_name: Optional[str] = Field(None, description="Name of the service")
    supplier_name: Optional[str] = Field(None, description="Supplier company name")
    termination_notice_period: Optional[str] = Field(None, description="Termination notice period details")
    UserEmail: Optional[str] = Field(None, description="User email address")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when record was created")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when record was last updated")

    class Config:
        # Example of how the data should look
        json_schema_extra = {
            "example": {
                "id": "c5d847a2-6fde-41d4-aaf3-b676ad3f8151",
                "contract_details": "所在地: 東京都港区三田三丁目５番１９号、面積: 5.19㎡(1.57坪)、月額金123,550円、支払期日: 翌月分を毎月20日までに支払",
                "contract_end_date": "2028/06/30",
                "contract_start_date": "2025/09/01",
                "customer_name": "ＦＰＴジャパンホールディングス株式会社",
                "LinkImage": "https://fptsoftware362-my.sharepoint.com/:b:/g/personal/tintt33_fpt_com/Efm3DWFRE89GqTJAnB7OV1UBzMiHtO3c_DQXlMbw5y7Udw",
                "service_name": "防災備蓄倉庫",
                "supplier_name": "住友不動産株式会社",
                "termination_notice_period": "契約期間満了の1年前から6ヶ月前まで",
                "UserEmail": "tintt33@fpt.com"
            }
        }


class ContractResponse(BaseModel):
    """
    Response model for contract operations
    """
    success: bool
    message: str
    contract_id: Optional[str] = None
    data: Optional[ContractData] = None


class ContractUpdateData(BaseModel):
    """
    Model for updating contract data (all fields optional except id)
    """
    contract_details: Optional[str] = None
    contract_end_date: Optional[str] = None
    contract_start_date: Optional[str] = None
    customer_name: Optional[str] = None
    LinkImage: Optional[str] = None
    service_name: Optional[str] = None
    supplier_name: Optional[str] = None
    termination_notice_period: Optional[str] = None
    UserEmail: Optional[str] = None
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
