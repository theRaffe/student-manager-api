from pydantic import BaseModel

class TeacherGroup(BaseModel):
    """
    Model of a teacher's group

    Attributes
    ----------
    groupId: uuid of the group
    name_course: str
        name of the course
    level: int
        represents first grade, second grade
    letter: str
        identifier of a group i.e. 1A, 2B
    start_period: int
        indicates year of begining to identify the group: 1B 2022 - 2023
    end_period: int
        indicates year of ending to identify the group: 3B 2022 - 2023
    """

    group_id: str
    name_course: str
    level: int
    letter: str
    start_period: int
    end_period: int

def convert_dict_group_model(group: dict):
    """
    To convert dict db into a TeacherGroup model

    Parameters
    ----------
    group: dict 
        raw data to convert into TeacherGroup

    Returns
    -------
    A model of TeacherGroup
    """
    return {
        "group_id": group["group_id"],
        "name_course": group["Course"]["name_course"],
        "letter": group["CatGroup"]["letter"],
        "level": group["CatGroup"]["level"],
        "end_period": group["CatGroup"]["end_period"],
        "start_period": group["CatGroup"]["start_period"]
    }
