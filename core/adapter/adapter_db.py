from datetime import datetime
from fastapi import HTTPException

from supabase import Client

from core.utils.default_utils import is_valid_uuid
from models.request.create_attendance_student import CreateAttendanceStudent
from models.request.create_new_group_course import CreateGroupCourse
from models.teacher_group import TeacherGroup, convert_dict_group_model
from postgrest.exceptions import APIError
import logging


class AdapterDB:
    supabase: Client

    def __init__(self, supabaseClient) -> None:
        self.supabase = supabaseClient

    def get_students(self):
        response = self.supabase.table("Student").select("*").execute()
        return response.data

    def get_attendance_by_group(self, group_id: str, init_range: str, end_range: str, teacher_id: str):
        rpc = self.supabase.rpc('get_attendance_group', {
            "in_group_id": group_id,
            "init_range": init_range,
            "end_range": end_range,
            "in_teacher_id": teacher_id
        })
        response = rpc.execute()
        return response

    def get_username_db(self, email: str):
        response = self.supabase.table("CatUser").select(
            "*").eq("email", email).execute()
        if len(response.data) > 0:
            return response.data[0]
        return None

    def get_teacher_group(self, teacher_id: str):
        response = self.supabase.from_("RelStudentGroupTeacher").select("""group_id,course_id,Course(name_course),CatGroup(level,letter,start_period,end_period)
        """).eq("teacher_id", teacher_id).execute()
        group_list = response.data
        result_group = [TeacherGroup(
            **convert_dict_group_model(group)) for group in group_list]
        return result_group

    def register_attendance(self, request: CreateAttendanceStudent):
        date_attendance = request.date_attendance if request.date_attendance else datetime.today(
        ).strftime('%Y-%m-%d')
        request_insert = {"student_group_id": request.student_group_id,
                          "course_id": request.course_id, "date_attendance": date_attendance}
        try:
            response = self.supabase.table(
                "StudentAttendance").insert(request_insert).execute()
            return response.data
        except APIError as exp:
            logging.error(exp)
            raise HTTPException(
                status_code=517, detail="An error occurred at DB operation")

    def get_basic_catalog(self, school_id: str):
        """
        Get rows of groups that belong to school_id parameter
        """

        if is_valid_uuid(school_id):
            responseCatGroup = self.supabase.table("CatGroup").select(
                "*").eq("school_id", school_id).execute()

            response = self.supabase.table("Course").select("*").execute()

            return {
                "cat_group": responseCatGroup.data,
                "cat_course": response.data
            }

        raise HTTPException(
            status_code=400, detail="Invalid UUID for school_id")

    def check_existing_group(self, groupRequest: CreateGroupCourse):
        """
        To check if group-course already exists

        Paramaters
        ----------
        groupRequest: CreateGroupCourse data to create a new group-course
        """
        response = self.supabase.from_("RelStudentGroupTeacher").select("*").eq("school_id", groupRequest.school_id).eq("group_id", groupRequest.group_id).eq("course_id", groupRequest.course_id).execute()
        return len(response.data) > 0

    def create_group_course_school(self, groupRequest: CreateGroupCourse, teacher_id: str):
        """
        To creata a new Group of student by teacher

        Parameters
        ----------
        groupRequest : CreateGroupCourse data to create a new group-course
        teacher_id : teacher to relate with the new group
        """
        insertRequest = { "school_id" : groupRequest.school_id, "group_id": groupRequest.group_id, "course_id": groupRequest.course_id, "teacher_id": teacher_id }
        try:
            response = self.supabase.table("RelStudentGroupTeacher").insert(insertRequest).execute()
            return response.data
        except APIError as exp:
            logging.error(exp)
            raise HTTPException(
                status_code=517, detail="An error occurred at DB operation")
