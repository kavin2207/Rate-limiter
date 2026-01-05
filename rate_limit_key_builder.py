from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from typing import Optional
import logging

@dataclass
class IdentifierResult:
    success: bool
    key: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    

class IdentifierPayload(BaseModel):
    user_id: Optional[str] = None
    api_key: Optional[str] = None
    ip: Optional[str] = None
    endpoint: str
    method: str
    metadata: Optional[Dict] = None


class RateLimiterBuilder:

    def key_builder(self, request):
        """
        Build a rate-limiting identifier key from FastAPI Request.

        Priority:
        1. User ID
        2. API Key
        3. IP Address
        """
        
        key = ""
        request = IdentifierPayload(
            user_id=request.headers.get("X-User-Id"),
            api_key=request.headers.get("X-Api-Key"),
            ip=request.client.host if request.client else None,
            endpoint=request.url.path,     # ✅ STRING
            method=request.method,          # ✅ STRING
            metadata=None
        )
        if request.user_id is not None:
            key = f"user:{request.user_id}:{request.endpoint}:{request.method.upper()}"
            return IdentifierResult(success=True,key=key)
        if request.api_key is not None:
            key = f"api_key:{request.api_key}:{request.endpoint}:{request.method.upper()}"
            return IdentifierResult(success=True,key=key)
        if request.ip is not None:
            key = f"ip:{request.ip}:{request.endpoint}:{request.method.upper()}"
            return IdentifierResult(success=True,key=key)
        
        return IdentifierResult(
            success=False,
            error_code="IDENTIFIER_NOT_FOUND",
            error_message="Request does not contain a valid rate-limit identity"
            )