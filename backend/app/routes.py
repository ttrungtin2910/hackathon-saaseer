from fastapi import APIRouter, HTTPException, Query, Path, Request
from typing import List, Optional
from app.models import ContractData, ContractResponse, ContractUpdateData
from app.database import cosmos_db
from config.settings import get_settings
from datetime import datetime, timedelta
import os
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


@router.get("/alerts/expiring", response_model=dict)
async def alert_expiring_contracts(
    user_email: str = Query(..., description="User email to filter contracts")
):
    """
    Check user's contracts and return alerts for those near expiry or missing end date.
    Returns list of dicts with fields: expired_status, report, contract_id.
    """
    try:
        settings = get_settings()
        # 1) Fetch contracts by user
        result = await cosmos_db.list_contracts_by_user(user_email, limit=1000)
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("message", "Failed to list contracts"))
        contracts = result.get("data", [])

        # Helper: parse date in formats YYYY/MM/DD or ISO
        def parse_date(value: Optional[str]) -> Optional[datetime]:
            if not value:
                return None
            for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
                try:
                    return datetime.strptime(value, fmt)
                except Exception:
                    continue
            return None

        # OpenAI config
        openai_key = settings.openai_api_key
        model = settings.openai_model
        use_ai = bool(openai_key)
        expiry_window_days = int(settings.expiry_warning_days)
        now = datetime.utcnow()
        window_end = now + timedelta(days=expiry_window_days)

        from textwrap import dedent

        def build_search_prompt(contract: dict) -> str:
            # Aggregate contract info into a concise context for web search
            fields = {
                "Service Name": contract.get("service_name"),
                "Supplier": contract.get("supplier_name"),
                "Customer": contract.get("customer_name"),
                "Details": contract.get("contract_details"),
                "Start Date": contract.get("contract_start_date"),
                "End Date": contract.get("contract_end_date"),
                "Termination Notice": contract.get("termination_notice_period"),
            }
            lines = [f"- {k}: {v}" for k, v in fields.items() if v]
            context = "\n".join(lines)
            template = dedent(
                f"""
                You are an analyst. Using web search, analyze the current contract context and propose alternatives.

                Current contract context:\n{context}

                Write a 500-800 word markdown report with these sections:
                1. CURRENT CONTRACT OVERVIEW (analysis, strengths/limitations)
                2. REQUIREMENTS ANALYSIS (user needs, current suitability)
                3. SIMILAR SERVICES IN THE MARKET (comparison, pros/cons of each option)
                4. RECOMMENDATIONS (most suitable solution, implementation roadmap)
                Output only the report, no preface or meta text. Don't place in code block.
                Please response as the context's language
                """
            ).strip()
            return template

        async def generate_report(contract: dict) -> str:
            if not use_ai:
                # Fallback stub if no API key configured
                return (
                    "## TỔNG QUAN HỢP ĐỒNG HIỆN TẠI\n\n"
                    "(Bản xem trước vì thiếu OPENAI_API_KEY)\n\n"
                    "## PHÂN TÍCH YÊU CẦU\n\n"
                    "## DỊCH VỤ TƯƠNG TỰ TRÊN THỊ TRƯỜNG\n\n"
                    "## KHUYẾN NGHỊ\n"
                )
            try:
                # Lazy import to avoid hard dependency if key missing
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                prompt = build_search_prompt(contract)
                response = client.responses.create(
                    model=model,
                    tools=[{"type": "web_search"}],
                    input=prompt,
                )
                # API per user's snippet provides output_text
                return getattr(response, "output_text", "") or ""
            except Exception as e:
                logger.error(f"AI report generation failed: {e}", exc_info=False)
                return "(Không thể tạo báo cáo tự động lúc này.)"

        results = []
        for c in contracts:
            end_dt = parse_date(c.get("contract_end_date"))
            near_expiry = False
            expired = False
            reason = ""
            if end_dt:
                if end_dt < now:
                    expired = True
                    near_expiry = True
                    reason = "expired"
                elif now <= end_dt <= window_end:
                    near_expiry = True
                    reason = "near_expiry"
            else:
                # missing end date triggers search
                near_expiry = True
                reason = "missing_end_date"
            
            near_expiry = True
            if near_expiry:
                report = await generate_report(c)
                results.append({
                    "contract_id": c.get("id"),
                    "expired_status": reason,
                    "report": report,
                })

        return {
            "success": True,
            "user_email": user_email,
            "count": len(results),
            "data": results,
            "expiry_window_days": expiry_window_days
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in alert_expiring_contracts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
