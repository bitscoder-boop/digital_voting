from pydantic import BaseModel
from typing import  List


class CandidateRegistration(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    age: int
    location: str
    face_encoded_list: List[float]
    vote_count: int = 0
