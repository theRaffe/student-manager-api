from pydantic import BaseModel

class CatUser(BaseModel):
    id: str
    email: str
    full_name: str
    role: int
    