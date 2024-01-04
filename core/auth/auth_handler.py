import os
import time
from fastapi import HTTPException, status

from jose import jwt, JWTError
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

JWT_SECRET = os.environ.get("SUPABASE_SECRET")
JWT_ALGORITHM = os.environ.get("ALGORITHM")

def decodeJWT(token: str) -> dict:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="An expception occurred at decoding JWT",
        headers={"WWW-Authenticate": "Bearer"})
    print("===== start decodeJWT")
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience="authenticated")
        print("check token exp:", decoded_token["exp"] >= time.time())
        result = decoded_token if decoded_token["exp"] >= time.time() else None
        return result
    except JWTError:
        raise exception
