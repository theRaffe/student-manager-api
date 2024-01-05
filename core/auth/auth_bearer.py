#
# @see https://testdriven.io/blog/fastapi-jwt-auth/
#
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            
            decoded_token = self.decode_jwt(credentials.credentials)
            if not self.verify_jwt(decoded_token):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return decoded_token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, decoded_token: dict) -> bool:
        isTokenValid: bool = False
        if decoded_token:
            isTokenValid = True
        return isTokenValid
    
    def decode_jwt(self, jwtoken: str) -> dict:
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        return payload
