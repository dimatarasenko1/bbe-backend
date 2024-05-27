from . import config
from fastapi import FastAPI, status, Response, Header, HTTPException
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from .utils.firebase_interactor import validate_user_login, validate_can_generate
from .models.quiz import DraftInput, DraftResponse, DraftOption, QuizDetails
from .utils import gpt_interactor, firebase_interactor
from . import generate

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://bbe-web.netlify.app",
    "https://play.bbenergy.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home(request: Request):
    return {"hello": "world"}


@app.post("/generate-draft", response_model=DraftResponse)
async def generate_draft(
    request: Request, payload: DraftInput, token: str = Header(...)
):
    user = validate_user_login(token)
    validate_can_generate(user)
    print(user)

    ok = gpt_interactor.moderation_check(payload.user_input)
    print(ok)
    if not ok:
        raise HTTPException(status_code=401, detail="Abusive content detected.")

    options = generate.generate_draft(payload.user_input)
    return DraftResponse(options=options)


@app.post("/generate-final", response_model=QuizDetails)
async def generate_final(
    request: Request, payload: DraftOption, token: str = Header(...)
):
    user = validate_user_login(token)
    validate_can_generate(user)
    print(user)

    # get username from firebase - save quiz with it later
    username = firebase_interactor.get_username(user["uid"])

    quizz = generate.generate_final(payload)
    quizz.username = username
    quizz_id = firebase_interactor.save_quizz(quizz)
    quizz.id = quizz_id

    # generates final quiz - saves to firestore
    return quizz


@app.post("/change-username")
async def change_username(
    request: Request, new_username: str, token: str = Header(...)
):
    user = validate_user_login(token)
    validate_can_generate(user)
    print(user)

    ## TODO
    # check if username is free
    # delete document with old username
    # make doc with new username
    # change username ref in all quizz docs
    # change username ref in all game docs

    return {"todo": "world"}


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check(response: Response):
    return {"status": True}
