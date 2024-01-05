from supabase import Client


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
        response = self.supabase.from_("RelStudentGroupTeacher").select("""groupId,Course(nameCourse),CatGroup(level,letter,start_period,end_period)
        """).eq("teacherId", teacher_id).execute()
        print("get_teacher_group: ", response.data)
        return response
