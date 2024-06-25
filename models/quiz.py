from .base import CamelCaseModel
from typing import List, Optional
from datetime import datetime
from pydantic import Field
from uuid import UUID, uuid4


class Question(CamelCaseModel):
    question: str
    answers: List[str]
    correctIndex: int


class Category(CamelCaseModel):
    slug: str
    emojiUnicode: Optional[str] = None


class QuizDetails(CamelCaseModel):
    id: Optional[str] = None
    created_at: datetime  # epoch timestamp
    updated_at: datetime
    title: str
    intro: str
    username: Optional[str] = "BBE Team"
    play_count: int = 1
    questions: List[Question]
    category: Optional[str] = "other"
    emoji: Optional[str] = None
    populated: Optional[bool] = True
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


class SupaQuiz(CamelCaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    intro: str
    username: str
    user_id: UUID
    play_count: int = 1
    category: Optional[str] = None
    emoji: Optional[str] = None
    questions: List[Question]
    created_at: datetime
    updated_at: datetime
    populated: bool = True
    seed: bool = False


class DraftInput(CamelCaseModel):
    user_input: str
    user_id: str


class DraftOption(CamelCaseModel):
    title: str
    example_question: str
    user_id: str


class DraftResponse(CamelCaseModel):
    options: List[DraftOption]
