from fastapi import Depends
from core.adapter.adapter_db import AdapterDB
from core.supabase.client_db import supabase_client 

from core.auth.auth_bearer import JWTBearer
from models.cat_user import CatUser

adapter_db = AdapterDB(supabaseClient=supabase_client)


def auth_user(decoded_token: dict = Depends(JWTBearer())):
    username = decoded_token["email"]

    username_dict = adapter_db.get_username_db(username)
    return CatUser(**username_dict)