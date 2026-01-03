from pydantic import BaseModel
from typing import Dict, List, Optional, Union

class identifierBuilder(BaseModel):
    user_id: Optional[str] = None
    api_key: Optional[str] = None
    ip: Optional[str] = None
    endpoint: str
    method: str
    metadata: Optional[Dict] = None


class RateLimiterBuilder:

    def key_builder(self, request):
        """
            This function is used to create rate limiter identifier and return the key 
            input : Json Payload 
            return : bool, <principal>:<endpoint>:<method>
        """
        request = identifierBuilder(**request)
        if request.user_id is not None:
            return True, f"user:{request.user_id}:{request.endpoint}:{request.method.upper()}"
        elif request.api_key is not None:
            return True, f"api_key:{request.api_key}:{request.endpoint}:{request.method.upper()}"
        elif request.ip is not None:
            return True, f"ip:{request.ip}:{request.endpoint}:{request.method.upper()}"
        else:
            return False, "Request Cannot Define User"