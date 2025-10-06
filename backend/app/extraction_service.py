import os
import logging
import json
import base64
from typing import Dict, Optional, Any, List
from openai import OpenAI
from pdf2image import convert_from_bytes
from PIL import Image
import io

logger = logging.getLogger(__name__)


class ContractExtractionService:
    """Service for extracting contract information using AI"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        
        self.client = OpenAI(api_key=self.openai_api_key)
        
        # Poppler path for Windows (optional)
        self.poppler_path = os.getenv("POPPLER_PATH", None)
        if self.poppler_path:
            logger.info(f"📌 Using custom Poppler path: {self.poppler_path}")
        
        # Auto-detect Poppler in local backend/poppler folder
        local_poppler = os.path.join(os.path.dirname(os.path.dirname(__file__)), "poppler", "Library", "bin")
        if os.path.exists(local_poppler) and not self.poppler_path:
            self.poppler_path = local_poppler
            logger.info(f"📌 Auto-detected local Poppler: {self.poppler_path}")
    
    def get_extraction_prompt(self) -> str:
        """Get the contract extraction prompt"""
        return """You are a contract data extraction system (input may be images/PDF, multi-page).  
Task: read the entire contract, find relevant clauses, and **return JSON only** with the following exact keys:

- `supplier_name`  
- `customer_name`  
- `contract_start_date`  
- `contract_end_date`  
- `termination_notice_period`  
- `contract_details`  
- `service_name`  

## Mandatory rules:
1. Values must be **short excerpts in the original contract language** (do not translate), except for `contract_start_date` and `contract_end_date` which must be **normalized into the format yyyy/mm/dd**.  
   - Example: "２０２５年９月１日" → "2025/09/01"  
   - Example: "２０２８年６月３０日" → "2028/06/30"  
2. If multiple candidates exist, select the value that applies to the **main contract** (not annexes or examples).  
3. If not found, return `null`. Do not guess.  
4. `termination_notice_period`: extract the exact clause that specifies how long in advance notice must be given for termination/non-renewal.  
5. `contract_details`: concise (1–2 sentences) in original language, summarizing subject, location/area, rent/amount, payment cycle—only if explicitly stated.  
6. `service_name`: extract the official name of the contracted service (e.g., "防災備蓄倉庫賃貸").  
7. `customer_name`: extract the official name of the customer/lessee/party receiving the service.  
8. **Do not** output explanations, notes, or markdown—return pure JSON.  

## Output format example:
{
  "supplier_name": "住友不動産株式会社",
  "customer_name": "〇〇株式会社",
  "contract_start_date": "2025/09/01",
  "contract_end_date": "2028/06/30",
  "termination_notice_period": "契約期間満了前の1年前から6か月前まで",
  "contract_details": "所在地: 東京都港区三田三丁目５番１９号、面積: 5.19㎡（1.57坪）、月額賃料: 23,550円、敷金: 282,000円、支払方法: 翌月分を毎月20日までに支払。",
  "service_name": "防災備蓄倉庫賃貸"
}"""
    
    def extract_from_pdf(self, file_content: bytes, file_name: str) -> Dict[str, Any]:
        """
        Extract contract information from PDF file by converting to images
        
        Args:
            file_content: Binary content of the PDF file
            file_name: Name of the file
            
        Returns:
            Dictionary with extracted contract information
        """
        try:
            logger.info(f"📄 Processing PDF file: {file_name}")
            logger.info(f"📊 PDF size: {len(file_content) / 1024:.2f} KB")
            
            # Convert PDF to images (one image per page)
            logger.info("🔄 Converting PDF pages to images...")
            
            # Use poppler_path if available
            if self.poppler_path:
                images = convert_from_bytes(
                    file_content, 
                    dpi=200, 
                    fmt='png',
                    poppler_path=self.poppler_path
                )
            else:
                images = convert_from_bytes(file_content, dpi=200, fmt='png')
                
            logger.info(f"✅ Converted PDF to {len(images)} page(s)")
            
            # Convert images to base64
            base64_images = []
            for idx, image in enumerate(images):
                # Convert PIL Image to bytes
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # Encode to base64
                base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
                base64_images.append(base64_image)
                logger.info(f"  📄 Page {idx + 1}: {len(img_byte_arr) / 1024:.2f} KB")
            
            # Use OpenAI Vision to extract information from all pages
            result = self._extract_with_vision_multipage(base64_images, file_name)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error extracting from PDF: {str(e)}")
            raise
    
    def extract_from_image(self, file_content: bytes, file_name: str) -> Dict[str, Any]:
        """
        Extract contract information from image file
        
        Args:
            file_content: Binary content of the image file
            file_name: Name of the file
            
        Returns:
            Dictionary with extracted contract information
        """
        try:
            logger.info(f"🖼️ Processing image file: {file_name}")
            
            # Encode image to base64
            base64_image = base64.b64encode(file_content).decode('utf-8')
            
            # Determine image format
            image_format = "jpeg"
            if file_name.lower().endswith('.png'):
                image_format = "png"
            elif file_name.lower().endswith('.gif'):
                image_format = "gif"
            elif file_name.lower().endswith('.webp'):
                image_format = "webp"
            
            # Use OpenAI Vision to extract information
            result = self._extract_with_vision(base64_image, image_format, file_name)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error extracting from image: {str(e)}")
            raise
    
    def _extract_with_vision(self, base64_image: str, image_format: str, file_name: str) -> Dict[str, Any]:
        """Extract contract information using OpenAI Vision API for images"""
        try:
            prompt = self.get_extraction_prompt()
            
            # Call OpenAI Vision API
            response = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a contract data extraction expert. Extract information accurately from images and return valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"{prompt}\n\n# This is the contract file: {file_name}"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_format};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            # Extract response
            response_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                # Remove first line (```json) and last line (```)
                response_text = "\n".join([line for line in lines[1:-1] if line.strip()])
            
            # Parse JSON
            extracted_data = json.loads(response_text)
            
            logger.info(f"✅ Successfully extracted contract information from image: {file_name}")
            logger.info(f"📊 Extracted data: {json.dumps(extracted_data, ensure_ascii=False, indent=2)}")
            
            return {
                "success": True,
                "data": extracted_data,
                "message": "Contract information extracted successfully from image"
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse JSON response: {str(e)}")
            logger.error(f"Response text: {response_text}")
            return {
                "success": False,
                "data": None,
                "message": f"Failed to parse AI response: {str(e)}"
            }
        except Exception as e:
            logger.error(f"❌ Error in vision extraction: {str(e)}")
            return {
                "success": False,
                "data": None,
                "message": f"Vision extraction failed: {str(e)}"
            }
    
    def _extract_with_vision_multipage(self, base64_images: List[str], file_name: str) -> Dict[str, Any]:
        """Extract contract information using OpenAI Vision API for multi-page documents"""
        try:
            prompt = self.get_extraction_prompt()
            
            # Build content with all pages
            content = [
                {
                    "type": "text",
                    "text": f"{prompt}\n\n# This is the contract file: {file_name}\n# Total pages: {len(base64_images)}"
                }
            ]
            
            # Add all pages as images
            for idx, base64_image in enumerate(base64_images):
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",
                        "detail": "high"  # Use high detail for better accuracy
                    }
                })
                logger.info(f"  📎 Added page {idx + 1} to AI request")
            
            # Call OpenAI Vision API with all pages
            logger.info("🤖 Sending all pages to OpenAI Vision API...")
            response = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a contract data extraction expert. Analyze all pages of the contract and extract information accurately. Return valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            # Extract response
            response_text = response.choices[0].message.content.strip()
            logger.info("✅ Received response from OpenAI")
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                # Remove first line (```json or ```) and last line (```)
                response_text = "\n".join([line for line in lines[1:-1] if line.strip()])
            
            # Parse JSON
            extracted_data = json.loads(response_text)
            
            logger.info(f"✅ Successfully extracted contract information from {len(base64_images)} page(s): {file_name}")
            logger.info(f"📊 Extracted data: {json.dumps(extracted_data, ensure_ascii=False, indent=2)}")
            
            return {
                "success": True,
                "data": extracted_data,
                "message": f"Contract information extracted successfully from {len(base64_images)} page(s)"
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse JSON response: {str(e)}")
            logger.error(f"Response text: {response_text}")
            return {
                "success": False,
                "data": None,
                "message": f"Failed to parse AI response: {str(e)}"
            }
        except Exception as e:
            logger.error(f"❌ Error in multi-page vision extraction: {str(e)}")
            return {
                "success": False,
                "data": None,
                "message": f"Multi-page vision extraction failed: {str(e)}"
            }
    
    def extract_from_file(self, file_content: bytes, file_name: str) -> Dict[str, Any]:
        """
        Extract contract information from any supported file type
        
        Args:
            file_content: Binary content of the file
            file_name: Name of the file
            
        Returns:
            Dictionary with extracted contract information
        """
        file_extension = os.path.splitext(file_name)[1].lower()
        
        if file_extension == '.pdf':
            return self.extract_from_pdf(file_content, file_name)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            return self.extract_from_image(file_content, file_name)
        else:
            return {
                "success": False,
                "data": None,
                "message": f"Unsupported file type: {file_extension}. Supported types: PDF, JPG, JPEG, PNG, GIF, WEBP"
            }


# Global instance
extraction_service = ContractExtractionService()

