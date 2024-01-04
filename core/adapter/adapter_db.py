from supabase import Client

class AdapterDB:
    supabase: Client

    def __init__(self, supabaseClient) -> None:
        self.supabase = supabaseClient

    def get_students(self):
        response = self.supabase.table("Student").select("*").execute()
        return response.data
    
    def get_attendance_by_group(self, group_id, init_range, end_range):
        rpc = self.supabase.rpc('get_attendance_group', {
            "in_group_id": group_id,
            "init_range" : init_range,
            "end_range": end_range, 
        })
        response = rpc.execute()
        return response

        