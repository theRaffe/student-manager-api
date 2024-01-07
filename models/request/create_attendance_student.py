
from typing import Optional
from pydantic import BaseModel


class CreateAttendanceStudent(BaseModel):
    """
    Request model to register an student's attendance

    Attributes
    ----------
    course_id: str
        uuid of the course
    student_group_id: str
        uuid of group - student(StudentGroup)
    date_attendance: str
        date to register with format YYYY-MM-DD
    """
    course_id: str
    student_group_id: str
    date_attendance: Optional[str] = None
