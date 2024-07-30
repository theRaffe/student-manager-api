
from pydantic import BaseModel


class CreateGroupCourse(BaseModel):
    """
    Request model to create a new group - course
    """
    course_id: str
    group_id: str
    school_id: str