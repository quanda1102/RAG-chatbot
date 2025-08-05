from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    question: str
    session_id: str

class Answer(BaseModel):
    answer: str
