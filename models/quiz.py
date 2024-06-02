from .base import CamelCaseModel
from typing import List, Optional


class Question(CamelCaseModel):
    question: str
    answers: List[str]
    correctIndex: int


class Category(CamelCaseModel):
    slug: str
    emojiUnicode: Optional[str] = None


class QuizDetails(CamelCaseModel):
    created_at: int  # epoch timestamp
    id: Optional[str] = None
    title: str
    intro: str
    username: str
    play_count: int = 1
    questions: List[Question]
    category: Optional[str] = "other"
    emoji: Optional[str] = None
    populated: bool = True
    seed: bool = False


class MockQuizDetails(CamelCaseModel):
    created_at: int  # epoch timestamp
    id: Optional[str] = None
    title: str
    username: str
    play_count: int = 1
    category: Optional[str] = "other"
    emoji: Optional[str] = None
    populated: bool = False
    seed: bool = False


class DraftInput(CamelCaseModel):
    user_input: str


class DraftOption(CamelCaseModel):
    title: str
    example_question: str


class DraftResponse(CamelCaseModel):
    options: List[DraftOption]
