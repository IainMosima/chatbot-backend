from typing import Any, Dict, Optional, TypeVar, Generic
from pydantic import BaseModel
from fastapi import HTTPException
import httpx
from typing import Union
import asyncio
from datetime import timedelta
import logging

T = TypeVar('T')


class ResponseWrapper(BaseModel, Generic[T]):
    """Wrapper for HTTP responses with type hints"""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    status_code: int


class HttpClient:
    """Helper class for making HTTP requests in FastAPI"""

    def __init__(
            self,
            base_url: str = "",
            timeout: int = 30,
            retry_attempts: int = 3,
            retry_delay: int = 1
    ):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)

    async def _make_request(
            self,
            method: str,
            endpoint: str,
            response_model: Optional[type] = None,
            **kwargs
    ) -> ResponseWrapper:
        """Make HTTP request with retries and error handling"""

        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint
        attempt = 0

        while attempt < self.retry_attempts:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.request(method, url, **kwargs)

                    # Raise for status but catch it in our error handling
                    response.raise_for_status()

                    if response_model and response.status_code != 204:
                        try:
                            data = response_model(**response.json())
                        except Exception as e:
                            self.logger.error(f"Response parsing error: {str(e)}")
                            raise HTTPException(
                                status_code=500,
                                detail="Error parsing response data"
                            )
                    else:
                        data = response.json() if response.content else None

                    return ResponseWrapper(
                        success=True,
                        data=data,
                        status_code=response.status_code
                    )

            except httpx.HTTPStatusError as e:
                if attempt == self.retry_attempts - 1:
                    return ResponseWrapper(
                        success=False,
                        error=str(e),
                        status_code=e.response.status_code
                    )

            except httpx.RequestError as e:
                if attempt == self.retry_attempts - 1:
                    raise HTTPException(
                        status_code=503,
                        detail=f"Service unavailable: {str(e)}"
                    )

            attempt += 1
            if attempt < self.retry_attempts:
                await asyncio.sleep(self.retry_delay * attempt)  # Exponential backoff

        return ResponseWrapper(
            success=False,
            error="Maximum retry attempts reached",
            status_code=500
        )

    async def get(
            self,
            endpoint: str,
            response_model: Optional[type] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> ResponseWrapper:
        """Make GET request"""
        return await self._make_request(
            'GET',
            endpoint,
            response_model=response_model,
            params=params,
            headers=headers
        )

    async def post(
            self,
            endpoint: str,
            response_model: Optional[type] = None,
            json: Optional[Dict[str, Any]] = None,
            data: Optional[Any] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> ResponseWrapper:
        """Make POST request"""
        return await self._make_request(
            'POST',
            endpoint,
            response_model=response_model,
            json=json,
            data=data,
            headers=headers
        )

    # Additional methods for PUT, DELETE, etc. can be added similarly