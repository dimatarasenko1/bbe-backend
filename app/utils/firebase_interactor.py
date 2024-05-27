import firebase_admin
from firebase_admin import auth
from fastapi import HTTPException
from ..config import db
from ..models.quiz import QuizDetails


def validate_user_login(token: str) -> dict:
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


def validate_can_generate(decoded_token: dict) -> bool:
    # later
    return True


def get_username(uid: str) -> str:
    query = db.collection("users").where("uid", "==", uid).stream()
    results = list(query)

    if not results:
        raise HTTPException(status_code=404, detail="No user found with the given UID")
    if len(results) > 1:
        raise HTTPException(
            status_code=400, detail="Multiple users found with the given UID"
        )

    # There should be exactly one document, return its ID (which is the username)
    user_doc = results[0]
    return user_doc.id


def save_quizz(quizz: QuizDetails) -> str:
    try:
        update_time, doc_ref = db.collection("quiz_details").add(quizz.model_dump())
        if update_time:
            print(update_time)
            return doc_ref.id
        else:
            raise Exception("Failed to write document.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save quiz")
