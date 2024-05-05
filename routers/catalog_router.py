from fastapi import APIRouter, Depends, HTTPException
from core.adapter.adapter_db import AdapterDB

from core.utils.auth_user_utils import auth_user
from models.cat_user import CatUser
from core.supabase.client_db import supabase_client

router = APIRouter(prefix="/catalog",
                   tags=["catalog"],
                   responses={404: {"message": "Route not found"}})

adapter_db = AdapterDB(supabaseClient=supabase_client)

@router.get("/get_group_by_school")
async def get_group_school(school_id: str, user:CatUser = Depends(auth_user)):
    """
    API to get list of student groups of authenticated user/teacher
    """
    response = adapter_db.get_group_by_school(school_id)
    return response
