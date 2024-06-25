from config import supabase
from models.quiz import SupaQuiz


def save_quiz(quiz: SupaQuiz) -> None:
    quiz_json = quiz.model_dump()
    quiz_json["id"] = str(quiz_json["id"])
    quiz_json["user_id"] = str(quiz_json["user_id"])
    del quiz_json["username"]
    del quiz_json["populated"]
    del quiz_json["created_at"]
    del quiz_json["updated_at"]
    supabase.table("Quizzes").insert(quiz_json).execute()
