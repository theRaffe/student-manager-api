from fastapi import APIRouter, Depends, HTTPException
from core.adapter.adapter_db import AdapterDB

from core.utils.auth_user_utils import auth_user
from models.cat_user import CatUser
from core.supabase.client_db import supabase_client
from models.request.create_new_group_course import CreateGroupCourse 

router = APIRouter(prefix="/teacher",
                   tags=["teacher"],
                   responses={404: {"message": "Route not found"}})

adapter_db = AdapterDB(supabaseClient=supabase_client)


@router.get("/groups")
async def get_groups(user:CatUser = Depends(auth_user)):
    """
    API to get list of student groups of authenticated user/teacher
    """
    response = adapter_db.get_teacher_group(user.id)
    return response

@router.get("/signed_user_data")
async def get_signed_user_data(user:CatUser = Depends(auth_user)):
    return user


@router.post("/create_new_group_course")
async def create_new_group_course(request: CreateGroupCourse, user:CatUser = Depends(auth_user)):
    """
    API to create a new group-course
    this API validates if group-course already exists

    Parameters
    ----------
    request: data to create a group-course
    """
    if adapter_db.check_existing_group(request):
        raise HTTPException(
                status_code=400, detail="The group-course already exists")
    return adapter_db.create_group_course_school(request, user.id)

