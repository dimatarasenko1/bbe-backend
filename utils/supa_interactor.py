from config import supabase
from models.quiz import SupaQuiz
from typing import Dict, Any


def save_quiz(quiz: SupaQuiz) -> None:
    quiz_json = quiz.model_dump()
    quiz_json["id"] = str(quiz_json["id"])
    quiz_json["user_id"] = str(quiz_json["user_id"])
    del quiz_json["username"]
    del quiz_json["populated"]
    del quiz_json["created_at"]
    del quiz_json["updated_at"]
    supabase.table("Quizzes").insert(quiz_json).execute()


def validate_user_login(token: str):
    resp = supabase.auth.get_user(token)
    print(resp)
    if "error" in resp:
        raise Exception("Token verification failed.")
    return resp.user


def delete_user(user_id: str):
    resp = supabase.auth.admin.delete_user(user_id)
    print(resp)
    if resp is not None:
        raise Exception("User deletion failed.")
