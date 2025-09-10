"""LangGraph OpenAI service for contract analysis and intelligent reporting"""

import json
import base64
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import openai
from openai import AzureOpenAI
from serpapi import GoogleSearch
import logging

from app.config import settings
from app.utils.prompts import (
    CONTRACT_EXTRACTION_PROMPT,
    SIMILAR_SERVICE_SEARCH_PROMPT,
    REPORT_GENERATION_PROMPT,
    FILE_CONTENT_EXTRACTION_PROMPT,
    DATA_VALIDATION_PROMPT,
    VISION_CONTRACT_EXTRACTION_PROMPT,
)
from app.models.contract import ExtractedContractData

logger = logging.getLogger(__name__)


class LangGraphService:
    """Service using LangGraph OpenAI for contract analysis and report generation"""

    def __init__(self):
        # Initialize Azure OpenAI client
        if settings.PROVIDER_NAME == "azure_openai":
            self.client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=settings.OPENAI_API_VERSION,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                timeout=settings.OPENAI_TIME_OUT,
            )
            self.model = settings.OPENAI_MODEL_NAME
            self.temperature = settings.AZ_OPENAI_TEMP
            self.max_tokens = settings.AZ_MAX_TOKEN
        else:
            # Fallback to regular OpenAI
            openai.api_key = settings.OPENAI_API_KEY
            self.client = openai
            self.model = settings.OPENAI_MODEL
            self.temperature = 0.1
            self.max_tokens = 1500

        self.serpapi_api_key = settings.SERPAPI_API_KEY
        logger.info(
            f"LangGraph service initialized with provider: {settings.PROVIDER_NAME}"
        )

    def extract_contract_data_from_file(
        self, file_data: bytes, file_type: str = None
    ) -> Tuple[bool, Optional[ExtractedContractData], str]:
        """
        Extract contract data directly from file using GPT-4 Vision

        Args:
            file_data: File data as bytes
            file_type: File type (optional, not used)

        Returns:
            Tuple[bool, Optional[ExtractedContractData], str]: (success, extracted_data, error_message)
        """
        try:
            # Send file directly to GPT-4 Vision for contract analysis
            return self._extract_contract_with_vision(file_data)

        except Exception as e:
            logger.error(f"Error extracting contract data from file: {e}")
            return False, None, f"Error: {str(e)}"

    def _extract_contract_with_vision(
        self, file_data: bytes
    ) -> Tuple[bool, Optional[ExtractedContractData], str]:
        """Use OpenAI GPT-4 Vision to extract contract data directly from file"""
        try:
            # Encode image to base64
            base64_image = base64.b64encode(file_data).decode("utf-8")

            # Use prompt from prompts file

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": VISION_CONTRACT_EXTRACTION_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            result_text = response.choices[0].message.content
            # Log only first part to avoid truncation, full JSON will be logged after cleaning
            logger.info(f"Raw vision response (first 200 chars): {result_text[:200]}...")

            # Preprocessing and parse JSON response
            try:
                # Clean response text (remove markdown if present)
                cleaned_text = self._clean_json_response(result_text)
                logger.info(f"Cleaned JSON text: {cleaned_text}")

                result_data = json.loads(cleaned_text)
                logger.info(f"Parsed JSON data keys: {list(result_data.keys())}")
                if 'Price' in result_data:
                    logger.info(f"Found Price in JSON: {result_data['Price']}")
                if 'Currency' in result_data:
                    logger.info(f"Found Currency in JSON: {result_data['Currency']}")

                # Preprocessing data
                processed_data = self._preprocess_contract_data(result_data)

                extracted_data = ExtractedContractData(**processed_data)
                logger.info(
                    "Contract data extracted and preprocessed successfully using vision"
                )
                return True, extracted_data, ""

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error from vision analysis: {e}")
                logger.error(f"Raw response: {result_text}")
                return False, None, f"Invalid JSON response: {str(e)}"
            except Exception as e:
                logger.error(f"Error processing extracted data: {e}")
                return False, None, f"Data processing error: {str(e)}"

        except Exception as e:
            logger.error(f"Error using OpenAI vision for contract analysis: {e}")
            return False, None, f"OpenAI vision error: {str(e)}"

    def _clean_json_response(self, response_text: str) -> str:
        """Clean and extract JSON from response text"""
        try:
            # Remove markdown code blocks if present
            if "```json" in response_text:
                start_idx = response_text.find("```json") + 7
                end_idx = response_text.find("```", start_idx)
                response_text = response_text[start_idx:end_idx]
            elif "```" in response_text:
                start_idx = response_text.find("```") + 3
                end_idx = response_text.find("```", start_idx)
                response_text = response_text[start_idx:end_idx]

            # Find JSON object boundaries
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx != -1 and end_idx != 0:
                response_text = response_text[start_idx:end_idx]

            return response_text.strip()
        except Exception as e:
            logger.warning(f"Error cleaning JSON response: {e}")
            return response_text.strip()

    def _preprocess_contract_data(self, data: dict) -> dict:
        """Preprocess and validate contract data"""
        try:
            logger.info(f"🔍 PREPROCESSING INPUT DATA: {data}")
            processed = {}

            # Process StartDate
            if data.get("StartDate"):
                processed["StartDate"] = self._normalize_date(data["StartDate"])

            # Process EndDate
            if data.get("EndDate"):
                processed["EndDate"] = self._normalize_date(data["EndDate"])

            # Process Provider (clean and normalize)
            if data.get("Provider"):
                processed["Provider"] = str(data["Provider"]).strip()

            # Process Service (clean and normalize)
            if data.get("Service"):
                processed["Service"] = str(data["Service"]).strip()

            # Process RenewalStatus (validate values)
            if data.get("RenewalStatus"):
                renewal_status = str(data["RenewalStatus"]).strip()
                valid_statuses = [
                    "Auto-Renewal",
                    "Manual-Renewal",
                    "No-Renewal",
                    "Unknown",
                ]
                if renewal_status in valid_statuses:
                    processed["RenewalStatus"] = renewal_status
                else:
                    processed["RenewalStatus"] = "Unknown"

            # Process Price (clean and validate)
            if data.get("Price") is not None:
                price = str(data["Price"]).strip()
                logger.info(f"Processing Price: '{price}' (original: {data.get('Price')})")
                if price and price.lower() != 'null':
                    processed["Price"] = price
                    logger.info(f"Added Price to processed: {price}")

            # Process Currency (clean and validate)
            if data.get("Currency") is not None:
                currency = str(data["Currency"]).strip().upper()
                logger.info(f"Processing Currency: '{currency}' (original: {data.get('Currency')})")
                if currency and currency.upper() != 'NULL':
                    processed["Currency"] = currency
                    logger.info(f"Added Currency to processed: {currency}")

            # Process SummaryContract (clean and limit length)
            if data.get("SummaryContract"):
                summary = str(data["SummaryContract"]).strip()
                # Limit to 500 characters max
                if len(summary) > 500:
                    summary = summary[:497] + "..."
                processed["SummaryContract"] = summary

            logger.info(f"🎯 FINAL PROCESSED DATA: {processed}")
            return processed

        except Exception as e:
            logger.error(f"Error preprocessing contract data: {e}")
            return data  # Return original data if preprocessing fails

    def _normalize_date(self, date_str: str) -> str:
        """Normalize date string to YYYY-MM-DD format"""
        try:
            from datetime import datetime

            date_str = str(date_str).strip()

            # Try common date formats
            date_formats = [
                "%Y-%m-%d",  # 2024-01-01
                "%d/%m/%Y",  # 01/01/2024
                "%m/%d/%Y",  # 01/01/2024
                "%d-%m-%Y",  # 01-01-2024
                "%Y/%m/%d",  # 2024/01/01
                "%B %d, %Y",  # January 1, 2024
                "%d %B %Y",  # 1 January 2024
            ]

            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    continue

            # If no format matches, return as is
            logger.warning(f"Could not normalize date: {date_str}")
            return date_str

        except Exception as e:
            logger.warning(f"Error normalizing date {date_str}: {e}")
            return str(date_str)

    def extract_contract_data(
        self, contract_content: str
    ) -> Tuple[bool, Optional[ExtractedContractData], str]:
        """
        Extract contract information from text content

        Args:
            contract_content: Contract content as text

        Returns:
            Tuple[bool, Optional[ExtractedContractData], str]: (success, extracted_data, error_message)
        """
        try:
            prompt = CONTRACT_EXTRACTION_PROMPT.format(
                contract_content=contract_content
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a contract analysis expert. Always respond in valid JSON format.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            result_text = response.choices[0].message.content

            # Parse JSON response
            try:
                result_data = json.loads(result_text)
                extracted_data = ExtractedContractData(**result_data)

                # Validate data
                validated_success, validated_data, _ = self._validate_extracted_data(
                    extracted_data.dict(), contract_content
                )

                if validated_success and validated_data:
                    final_data = ExtractedContractData(**validated_data)
                    return True, final_data, ""

                return True, extracted_data, ""

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                return False, None, f"Invalid JSON response: {str(e)}"

        except Exception as e:
            logger.error(f"Error extracting contract data: {e}")
            return False, None, f"Error: {str(e)}"

    def _validate_extracted_data(
        self, extracted_data: Dict, original_content: str
    ) -> Tuple[bool, Optional[Dict], str]:
        """Validate and normalize extracted data"""
        try:
            prompt = DATA_VALIDATION_PROMPT.format(
                extracted_data=json.dumps(extracted_data, indent=2),
                original_content=original_content[:2000],  # Limit content length
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data validation expert. Always respond in valid JSON format.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            result_text = response.choices[0].message.content
            validated_data = json.loads(result_text)

            return True, validated_data, ""

        except Exception as e:
            logger.error(f"Error validating data: {e}")
            return False, None, f"Validation error: {str(e)}"

    def search_similar_services(
        self, provider: str, service: str, user_requirement: str
    ) -> Tuple[bool, List[Dict], str]:
        """
        Search for similar services on the web

        Args:
            provider: Service provider
            service: Service type
            user_requirement: User requirement

        Returns:
            Tuple[bool, List[Dict], str]: (success, search_results, error_message)
        """
        try:
            # Generate search keywords
            keywords_success, search_keywords, _ = self._generate_search_keywords(
                provider, service, user_requirement
            )

            if not keywords_success:
                return False, [], "Failed to generate search keywords"

            # Perform web search for each keyword
            all_results = []
            for keyword in search_keywords:
                web_success, web_results, _ = self._perform_web_search(keyword)
                if web_success:
                    all_results.extend(web_results)

            # Remove duplicates and limit results
            unique_results = []
            seen_urls = set()
            for result in all_results:
                if result.get("url", "") not in seen_urls:
                    seen_urls.add(result.get("url", ""))
                    unique_results.append(result)
                    if len(unique_results) >= 10:  # Limit to top 10
                        break

            return True, unique_results, ""

        except Exception as e:
            logger.error(f"Error searching similar services: {e}")
            return False, [], f"Error: {str(e)}"

    def _generate_search_keywords(
        self, provider: str, service: str, user_requirement: str
    ) -> Tuple[bool, List[str], str]:
        """Generate search keywords"""
        try:
            prompt = SIMILAR_SERVICE_SEARCH_PROMPT.format(
                provider=provider or "Unknown",
                service=service or "Unknown",
                start_date="N/A",
                end_date="N/A",
                user_requirement=user_requirement,
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a search expert. Always respond with a JSON array of strings.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            result_text = response.choices[0].message.content
            keywords = json.loads(result_text)

            return True, keywords, ""

        except Exception as e:
            logger.error(f"Error generating search keywords: {e}")
            return False, [], f"Error: {str(e)}"

    def _perform_web_search(self, query: str) -> Tuple[bool, List[Dict], str]:
        """Perform web search using SerpAPI"""
        try:
            search = GoogleSearch(
                {
                    "q": query,
                    "api_key": self.serpapi_api_key,
                    "num": 5,  # Number of results
                    "hl": "en",  # Language
                    "gl": "us",  # Country
                    "safe": "active",  # Safe search
                }
            )

            search_results = search.get_dict()

            # Extract relevant information from organic results
            results = []
            if "organic_results" in search_results:
                for item in search_results["organic_results"]:
                    results.append(
                        {
                            "title": item.get("title", ""),
                            "url": item.get("link", ""),
                            "snippet": item.get("snippet", ""),
                            "position": item.get("position", 0),
                        }
                    )

            logger.info(
                f"SerpAPI search completed for query: {query}, found {len(results)} results"
            )
            return True, results, ""

        except Exception as e:
            logger.error(f"Error performing SerpAPI search: {e}")
            return False, [], f"SerpAPI search error: {str(e)}"

    def generate_report(
        self, contract_data: Dict, user_requirement: str, similar_services: List[Dict]
    ) -> Tuple[bool, str, str]:
        """
        Generate comprehensive report

        Args:
            contract_data: Current contract information
            user_requirement: User requirement
            similar_services: List of similar services

        Returns:
            Tuple[bool, str, str]: (success, report, error_message)
        """
        try:
            # Format similar services data
            services_text = ""
            for i, service in enumerate(similar_services, 1):
                services_text += f"{i}. {service.get('title', 'N/A')}\n"
                services_text += f"   URL: {service.get('url', 'N/A')}\n"
                services_text += f"   Mô tả: {service.get('snippet', 'N/A')}\n\n"

            prompt = REPORT_GENERATION_PROMPT.format(
                provider=contract_data.get("Provider", "Unknown"),
                service=contract_data.get("Service", "Unknown"),
                start_date=contract_data.get("StartDate", "N/A"),
                end_date=contract_data.get("EndDate", "N/A"),
                renewal_status=contract_data.get("RenewalStatus", "Unknown"),
                user_requirement=user_requirement,
                similar_services=(
                    services_text
                    if services_text
                    else "Không tìm thấy dịch vụ tương tự."
                ),
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional business consultant. Generate detailed, helpful reports in Vietnamese.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            report = response.choices[0].message.content
            return True, report, ""

        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return False, "", f"Error: {str(e)}"


# Global service instance
langgraph_service = LangGraphService()
