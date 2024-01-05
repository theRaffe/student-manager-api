from fastapi import APIRouter, Depends, HTTPException
from core.adapter.adapter_db import AdapterDB

from core.utils.auth_user_utils import auth_user
from models.cat_user import CatUser
from core.supabase.client_db import supabase_client 

router = APIRouter(prefix="/teacher",
                   tags=["teacher"],
                   responses={404: {"message": "Route not found"}})

adapter_db = AdapterDB(supabaseClient=supabase_client)


@router.get("/groups")
async def get_groups(user:CatUser = Depends(auth_user)):
    response = adapter_db.get_teacher_group(user.id)
    return response
