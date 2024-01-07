from fastapi import APIRouter, Depends

from core.adapter.adapter_db import AdapterDB
from core.auth.auth_bearer import JWTBearer
from core.supabase.client_db import supabase_client
from core.utils.auth_user_utils import auth_user
from models.cat_user import CatUser
from models.request.create_attendance_student import CreateAttendanceStudent

adapter_db = AdapterDB(supabaseClient=supabase_client)

router = APIRouter(prefix="/students",
                   tags=["students"],
                   responses={404: {"message": "Data not found"}})

@router.get("/")
async def get_students():
    return adapter_db.get_students()

@router.get("/attendance")
async def get_attendance_group(group_id: str, init_range: str, end_range: str,user: CatUser = Depends(auth_user)):
    """
    This is an API to get student group's attendance by a period of time of a group that belongs to current user(teacher)
    
    Parameters
    ----------
    group_id: str
        uuid of group to get data
    init_range: str 
        a string of initial date of range
    end_range: str
        a string of end date of range
    """
    return adapter_db.get_attendance_by_group(group_id, init_range, end_range, user.id)

@router.post("/register-attendance", dependencies=[Depends(JWTBearer())])
async def register_attendance(request: CreateAttendanceStudent):
    response = adapter_db.register_attendance(request=request)
    return response
