from .base import CamelCaseModel
from typing import List, Optional


class Question(CamelCaseModel):
    question: str
    answers: List[str]
    correctIndex: int


class QuizDetails(CamelCaseModel):
    id: Optional[str] = None
    title: str
    intro: str
    username: Optional[str] = None
    play_count: int = 1
    questions: List[Question]


class DraftInput(CamelCaseModel):
    user_input: str


class DraftOption(CamelCaseModel):
    title: str
    example_question: str


class DraftResponse(CamelCaseModel):
    options: List[DraftOption]
