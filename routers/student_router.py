from fastapi import APIRouter, Depends, HTTPException
from core.auth.auth_bearer import JWTBearer
from core.supabase.client_db import supabase_client 

from core.adapter.adapter_db import AdapterDB

adapter_db = AdapterDB(supabaseClient=supabase_client)

router = APIRouter(prefix="/students",
                   tags=["students"],
                   responses={404: {"message": "Data not found"}})

@router.get("/")
async def get_students():
    return adapter_db.get_students()

@router.get("/attendance", dependencies=[Depends(JWTBearer())])
async def get_attendance_group(group_id: str, init_range: str, end_range: str):
    # print("****DEBUG dependencies", dependencies)
    return adapter_db.get_attendance_by_group(group_id, init_range, end_range)
    # return { "res": "OK"}