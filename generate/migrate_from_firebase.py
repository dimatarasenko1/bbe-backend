# load all from firebase
# push to supabase
from postgrest.exceptions import APIError
from utils.firebase_interactor import load_quizzes
from config import supabase


def migrate():
    quizzes = load_quizzes()
    print(len(quizzes))
    # print(quizzes)
    for quiz in quizzes:
        try:
            quiz_json = quiz.model_dump()
            del quiz_json["id"]
            del quiz_json["created_at"]
            del quiz_json["username"]
            del quiz_json["populated"]
            supabase.table("Quizzes").insert(quiz_json).execute()
        except APIError:
            print("Failed to migrate quiz")
            continue
