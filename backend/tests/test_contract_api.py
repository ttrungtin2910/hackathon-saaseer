#!/usr/bin/env python3
"""
Test script to demonstrate sending contract data to the FastAPI backend
"""

import httpx
import json
import asyncio
from typing import Dict, Any
from config.settings import get_settings

# Get settings
settings = get_settings()

# Configuration
API_BASE_URL = f"http://{settings.host}:{settings.port}"
CONTRACTS_ENDPOINT = f"{API_BASE_URL}/api/v1/contracts/quick-create"

# Sample contract data (from user's request)
SAMPLE_CONTRACT_DATA = {
    "contract_details": "所在地: 東京都港区三田三丁目５番１９号、面積: 5.19㎡(1.57坪)、月額金123,550円、支払期日: 翌月分を毎月20日までに支払",
    "contract_end_date": "2028/06/30",
    "contract_start_date": "2025/09/01",
    "customer_name": "ＦＰＴジャパンホールディングス株式会社",
    "id": "c5d847a2-6fde-41d4-aaf3-b676ad3f8151",
    "LinkImage": "https://fptsoftware362-my.sharepoint.com/:b:/g/personal/tintt33_fpt_com/Efm3DWFRE89GqTJAnB7OV1UBzMiHtO3c_DQXlMbw5y7Udw",
    "service_name": "防災備蓄倉庫",
    "supplier_name": "住友不動産株式会社",
    "termination_notice_period": "契約期間満了の1年前から6ヶ月前まで",
    "UserEmail": "tintt33@fpt.com"
}


async def test_api_health():
    """Test API health check"""
    print("🔍 Testing API health...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/health")
            if response.status_code == 200:
                print("✅ API is healthy")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ API health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {str(e)}")
        return False


async def create_contract(contract_data: Dict[str, Any]):
    """Create a contract using the quick-create endpoint"""
    print("\n📝 Creating contract...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CONTRACTS_ENDPOINT,
                json=contract_data,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Contract created successfully!")
                print(f"   Contract ID: {result.get('contract_id')}")
                print(f"   Message: {result.get('message')}")
                return result
            else:
                print(f"❌ Failed to create contract: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
    except Exception as e:
        print(f"❌ Error creating contract: {str(e)}")
        return None


async def get_contract(contract_id: str, user_email: str):
    """Retrieve a contract by ID"""
    print(f"\n🔍 Retrieving contract {contract_id}...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/api/v1/contracts/{contract_id}",
                params={"user_email": user_email},
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Contract retrieved successfully!")
                print(f"   Customer: {result['data']['customer_name']}")
                print(f"   Service: {result['data']['service_name']}")
                return result
            else:
                print(f"❌ Failed to retrieve contract: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
    except Exception as e:
        print(f"❌ Error retrieving contract: {str(e)}")
        return None


async def list_contracts(user_email: str):
    """List all contracts for a user"""
    print(f"\n📋 Listing contracts for {user_email}...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/api/v1/contracts/",
                params={"user_email": user_email, "limit": 10},
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Found {result.get('count', 0)} contracts")
                for i, contract in enumerate(result.get('data', []), 1):
                    print(f"   {i}. {contract['id']} - {contract['service_name']}")
                return result
            else:
                print(f"❌ Failed to list contracts: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
    except Exception as e:
        print(f"❌ Error listing contracts: {str(e)}")
        return None


async def main():
    """Main test function"""
    print("🚀 Starting SaaSeer Contract API Test")
    print("=" * 50)
    
    # Test API health
    if not await test_api_health():
        print("\n❌ API is not available. Please make sure the server is running.")
        print("   Run: python main.py")
        return
    
    # Create contract
    contract_result = await create_contract(SAMPLE_CONTRACT_DATA)
    if not contract_result:
        print("\n❌ Failed to create contract. Test stopped.")
        return
    
    contract_id = contract_result.get('contract_id')
    user_email = SAMPLE_CONTRACT_DATA['UserEmail']
    
    # Retrieve the created contract
    await get_contract(contract_id, user_email)
    
    # List all contracts for the user
    await list_contracts(user_email)
    
    print("\n" + "=" * 50)
    print("✅ Test completed successfully!")
    print("\n📖 API Documentation available at:")
    print(f"   • Interactive docs: {API_BASE_URL}/docs")
    print(f"   • ReDoc: {API_BASE_URL}/redoc")


if __name__ == "__main__":
    print("Starting contract API test...")
    print(f"Make sure your FastAPI server is running on {API_BASE_URL}")
    print("Press Ctrl+C to cancel")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
