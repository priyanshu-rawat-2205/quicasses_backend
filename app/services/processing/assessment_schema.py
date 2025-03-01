from pydantic import BaseModel

class Question(BaseModel):
    title: str
    options: list[str]
    correct_option: int

class Assessment(BaseModel):
    title: str
    description: str
    questions: list[Question]
