"""API endpoints for Contract Management system"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import logging
import uuid
from datetime import datetime

from app.models.contract import (
    ContractInformation,
    UserRequirement,
    ContractListResponse,
    ContractSearchRequest,
    ContractSearchResponse,
    ContractInsertResponse,
)
from app.services.cosmosdb import cosmosdb_service
from app.services.azure_blob import azure_blob_service
from app.services.langgraph import langgraph_service

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1", tags=["contracts"])


@router.get("/contracts/{username}", response_model=ContractListResponse)
async def list_contracts_by_username(username: str):
    """
    API: List contracts by UserName

    Args:
        username: User name

    Returns:
        ContractListResponse: List of contracts and total count
    """
    try:
        logger.info(f"Getting contracts for user: {username}")

        # Get contracts list from CosmosDB
        contracts = cosmosdb_service.get_contracts_by_username(username)

        response = ContractListResponse(contracts=contracts, total=len(contracts))

        logger.info(f"Found {len(contracts)} contracts for user: {username}")
        return response

    except Exception as e:
        logger.error(f"Error listing contracts for {username}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/contracts/upload", response_model=ContractInsertResponse)
async def insert_contract(username: str = Form(...), file: UploadFile = File(...)):
    """
    API: Insert contract

    Args:
        username: User name
        file: File upload (image, PDF or scanned PDF)

    Returns:
        ContractInsertResponse: Insert result and extracted information
    """
    try:
        logger.info(f"Uploading contract for user: {username}, file: {file.filename}")

        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Read file data
        file_data = await file.read()
        if not file_data:
            raise HTTPException(status_code=400, detail="Empty file")

        # Upload file to Azure Blob Storage
        upload_success, blob_url = azure_blob_service.upload_file(
            file_data=file_data,
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
        )

        if not upload_success:
            raise HTTPException(
                status_code=500, detail=f"File upload failed: {blob_url}"
            )

        logger.info(f"File uploaded successfully: {blob_url}")

        # Extract contract data directly from file using LangGraph
        data_success, extracted_data, data_error = (
            langgraph_service.extract_contract_data_from_file(file_data=file_data)
        )

        contract_data = None
        if data_success and extracted_data:
            contract_data = extracted_data.dict()
            logger.info(f"Contract data extracted successfully")
        else:
            logger.warning(f"Contract data extraction failed: {data_error}")

        # Create contract information object
        contract = ContractInformation(
            UserName=username,
            ContractFilePath=blob_url,
            StartDate=None,
            EndDate=None,
            Provider=None,
            Service=None,
            RenewalStatus=None,
        )

        # Update with extracted data if available
        if contract_data:
            if contract_data.get("StartDate"):
                try:
                    contract.StartDate = datetime.fromisoformat(
                        contract_data["StartDate"]
                    )
                except:
                    pass
            if contract_data.get("EndDate"):
                try:
                    contract.EndDate = datetime.fromisoformat(contract_data["EndDate"])
                except:
                    pass
            contract.Provider = contract_data.get("Provider")
            contract.Service = contract_data.get("Service")
            contract.RenewalStatus = contract_data.get("RenewalStatus")
            contract.SummaryContract = contract_data.get("SummaryContract")

        # Insert to CosmosDB
        insert_success = cosmosdb_service.insert_contract(contract)

        if not insert_success:
            # Clean up uploaded file if database insert fails
            azure_blob_service.delete_file(blob_url)
            raise HTTPException(
                status_code=500, detail="Failed to save contract to database"
            )

        logger.info(f"Contract inserted successfully: {contract.ContractID}")

        response = ContractInsertResponse(
            success=True,
            contract_id=contract.ContractID,
            message="Contract uploaded and processed successfully",
            extracted_data=contract_data,
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inserting contract: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/contracts/search", response_model=ContractSearchResponse)
async def search_contract(request: ContractSearchRequest):
    """
    API: Search contract

    Args:
        request: ContractSearchRequest with UserName, ContractID, UserRequirementContent

    Returns:
        ContractSearchResponse: Comprehensive report and similar service information
    """
    try:
        logger.info(
            f"Searching contract for user: {request.UserName}, contract: {request.ContractID}"
        )

        # Validate contract exists and belongs to user
        contract = cosmosdb_service.get_contract_by_id(request.ContractID)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        if contract.UserName != request.UserName:
            raise HTTPException(
                status_code=403,
                detail="Access denied: Contract does not belong to user",
            )

        # Save user requirement
        user_requirement = UserRequirement(
            UserRequirementContent=request.UserRequirementContent,
            ContractID=request.ContractID,
        )

        requirement_success = cosmosdb_service.insert_user_requirement(user_requirement)
        if not requirement_success:
            logger.warning(
                "Failed to save user requirement, but continuing with search"
            )

        # Search for similar services
        search_success, similar_services, search_error = (
            langgraph_service.search_similar_services(
                provider=contract.Provider or "",
                service=contract.Service or "",
                user_requirement=request.UserRequirementContent,
            )
        )

        if not search_success:
            logger.warning(f"Similar services search failed: {search_error}")
            similar_services = []

        # Prepare contract data for report
        contract_data = {
            "Provider": contract.Provider,
            "Service": contract.Service,
            "StartDate": contract.StartDate.isoformat() if contract.StartDate else None,
            "EndDate": contract.EndDate.isoformat() if contract.EndDate else None,
            "RenewalStatus": contract.RenewalStatus,
        }

        # Generate report using LangGraph
        report_success, report, report_error = langgraph_service.generate_report(
            contract_data=contract_data,
            user_requirement=request.UserRequirementContent,
            similar_services=similar_services,
        )

        if not report_success:
            logger.error(f"Report generation failed: {report_error}")
            report = f"Không thể tạo báo cáo: {report_error}"

        logger.info(f"Search completed successfully for contract: {request.ContractID}")

        response = ContractSearchResponse(
            success=True,
            report=report,
            user_requirement_id=user_requirement.UserRequirementID,
            similar_services=similar_services,
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching contract: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/contracts/{contract_id}/requirements")
async def get_contract_requirements(contract_id: str):
    """
    API: Get contract requirements list

    Args:
        contract_id: Contract ID

    Returns:
        List[UserRequirement]: List of requirements
    """
    try:
        logger.info(f"Getting requirements for contract: {contract_id}")

        # Check if contract exists
        contract = cosmosdb_service.get_contract_by_id(contract_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        # Get requirements
        requirements = cosmosdb_service.get_requirements_by_contract_id(contract_id)

        logger.info(
            f"Found {len(requirements)} requirements for contract: {contract_id}"
        )
        return requirements

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting contract requirements: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/contracts/{contract_id}/download")
async def download_contract_file(contract_id: str):
    """
    API: Generate contract file download link

    Args:
        contract_id: Contract ID

    Returns:
        dict: Time-limited download URL
    """
    try:
        logger.info(f"Generating download link for contract: {contract_id}")

        # Get contract
        contract = cosmosdb_service.get_contract_by_id(contract_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        # Generate download URL
        url_success, download_url, url_error = azure_blob_service.generate_download_url(
            blob_url=contract.ContractFilePath, expiry_hours=24
        )

        if not url_success:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate download URL: {url_error}",
            )

        return {
            "download_url": download_url,
            "expires_in_hours": 24,
            "contract_id": contract_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating download link: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Contract Management API",
    }
