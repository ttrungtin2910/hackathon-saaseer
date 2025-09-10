from fastapi import APIRouter, HTTPException, Query, Path, Request
from typing import List, Optional
from app.models import ContractData, ContractResponse, ContractUpdateData
from app.database import cosmos_db
import logging
import json

logger = logging.getLogger(__name__)

# Create router for contract operations
router = APIRouter(prefix="/api/v1/contracts", tags=["contracts"])


@router.post("/", response_model=ContractResponse, status_code=201)
async def create_contract(request: Request):
    """
    Create a new contract in Azure Cosmos DB
    
    - **contract_data**: Contract information including all required fields
    
    Returns the created contract data with success status
    """
    try:
        # Parse JSON and handle wrapped data format
        body = await request.body()
        import json
        raw_data = json.loads(body.decode('utf-8'))
        
        # Check if data is wrapped in "contract_data" field
        if "contract_data" in raw_data and isinstance(raw_data["contract_data"], str):
            # Parse the inner JSON string
            contract_json = json.loads(raw_data["contract_data"])
            raw_data = contract_json
        elif "contract_data" in raw_data and isinstance(raw_data["contract_data"], dict):
            raw_data = raw_data["contract_data"]
        
        # Create ContractData model
        try:
            contract_data = ContractData(**raw_data)
        except Exception as validation_error:
            logger.error(f"❌ Validation error: {validation_error}")
            raise HTTPException(status_code=422, detail=f"Validation error: {validation_error}")
        
        # Log contract creation process
        logger.info(f"📝 Creating contract: {contract_data.id}")
        logger.info(f"👤 Customer: {contract_data.customer_name or 'N/A'}")
        logger.info(f"🏢 Service: {contract_data.service_name or 'N/A'}")
        
        result = await cosmos_db.create_contract(contract_data)
        
        if result["success"]:
            return ContractResponse(
                success=True,
                message=result["message"],
                contract_id=contract_data.id,
                data=ContractData(**result["data"])
            )
        else:
            raise HTTPException(status_code=409, detail=result["message"])
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error creating contract: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: str = Path(..., description="Contract ID"),
    user_email: str = Query(..., description="User email (partition key)")
):
    """
    Retrieve a specific contract by ID and user email
    
    - **contract_id**: Unique identifier of the contract
    - **user_email**: Email of the user (used as partition key)
    
    Returns the contract data if found
    """
    try:
        result = await cosmos_db.get_contract(contract_id, user_email)
        
        if result["success"]:
            return ContractResponse(
                success=True,
                message=result["message"],
                contract_id=contract_id,
                data=ContractData(**result["data"])
            )
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving contract: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{contract_id}", response_model=ContractResponse)
async def update_contract(
    update_data: ContractUpdateData,
    contract_id: str = Path(..., description="Contract ID"),
    user_email: str = Query(..., description="User email (partition key)")
):
    """
    Update an existing contract
    
    - **contract_id**: Unique identifier of the contract
    - **user_email**: Email of the user (used as partition key)
    - **update_data**: Fields to update (only provided fields will be updated)
    
    Returns the updated contract data
    """
    try:
        result = await cosmos_db.update_contract(contract_id, user_email, update_data)
        
        if result["success"]:
            return ContractResponse(
                success=True,
                message=result["message"],
                contract_id=contract_id,
                data=ContractData(**result["data"])
            )
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating contract: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{contract_id}", response_model=ContractResponse)
async def delete_contract(
    contract_id: str = Path(..., description="Contract ID"),
    user_email: str = Query(..., description="User email (partition key)")
):
    """
    Delete a contract by ID and user email
    
    - **contract_id**: Unique identifier of the contract
    - **user_email**: Email of the user (used as partition key)
    
    Returns success status
    """
    try:
        result = await cosmos_db.delete_contract(contract_id, user_email)
        
        if result["success"]:
            return ContractResponse(
                success=True,
                message=result["message"],
                contract_id=contract_id
            )
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting contract: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=dict)
async def list_contracts(
    user_email: str = Query(..., description="User email to filter contracts"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of contracts to return")
):
    """
    List all contracts for a specific user
    
    - **user_email**: Email of the user to filter contracts
    - **limit**: Maximum number of contracts to return (1-1000, default: 100)
    
    Returns a list of contracts for the specified user
    """
    try:
        result = await cosmos_db.list_contracts_by_user(user_email, limit)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "data": result["data"],
                "count": result["count"],
                "user_email": user_email
            }
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error listing contracts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Health check endpoint specifically for contracts
@router.get("/health/status")
async def health_check():
    """
    Health check endpoint for the contracts service
    """
    return {
        "status": "healthy",
        "service": "contracts",
        "message": "Contract service is running"
    }
