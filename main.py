import config
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    status,
    Response,
    Header,
    HTTPException,
    Query,
)
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from utils.firebase_interactor import validate_user_login, validate_can_generate
from models.quiz import (
    DraftInput,
    DraftResponse,
    DraftOption,
    QuizDetails,
    MockQuizDetails,
    SupaQuiz,
)
from utils import gpt_interactor, firebase_interactor, supa_interactor
import generate
import services
from typing import Dict, List, Optional

app = FastAPI()
connected_pairs: Dict[str, List[WebSocket]] = {}

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


@app.get("/quizzes")
async def quizzes(
    request: Request,
    query: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: Optional[int] = Query(1),
    seen: Optional[List[str]] = Query([]),
):
    return services.get_quizzes(page, query, category, seen)


@app.post("/generate-draft", response_model=DraftResponse)
async def generate_draft(
    request: Request, payload: DraftInput, token: str = Header(...)
):
    print(payload.user_id)
    # user = validate_user_login(token)
    # validate_can_generate(user)
    # print(user)

    ok = gpt_interactor.moderation_check(payload.user_input)
    print(ok)
    if not ok:
        raise HTTPException(status_code=401, detail="Abusive content detected.")

    options = generate.generate_draft(payload)
    return DraftResponse(options=options)


@app.post("/generate-final", response_model=SupaQuiz)
async def generate_final(
    request: Request, payload: DraftOption, token: str = Header(...)
):
    # user = validate_user_login(token)
    # validate_can_generate(user)

    quizz = generate.generate_final(payload)
    cat = generate.assign_category(quizz.title)
    quizz.category = cat.slug
    quizz.emoji = cat.emojiUnicode
    supa_interactor.save_quiz(quizz)

    return quizz


@app.post("/populate-quizz", response_model=QuizDetails)
async def populate_quizz(request: Request, payload: MockQuizDetails):
    quizz = generate.populate_quizz(payload)
    firebase_interactor.reassign_quizz(quizz)
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


@app.websocket("/ws/{game_id}/{user_id}")
async def websocket_endpoint(game_id: str, user_id: str, websocket: WebSocket):
    await websocket.accept()

    # Initialize the pair if not present
    if game_id not in connected_pairs:
        connected_pairs[game_id] = []

    # Add the WebSocket connection to the pair
    connected_pairs[game_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Send the received data to the other user in the same pair
            for ws in connected_pairs[game_id]:
                if ws != websocket:
                    await ws.send_text(data)
    except WebSocketDisconnect:
        # If a user disconnects, remove them from the pair
        connected_pairs[game_id].remove(websocket)
        if not connected_pairs[game_id]:
            del connected_pairs[game_id]
    except Exception as e:
        print(f"Unexpected error: {e}")


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check(response: Response):
    return {"status": True}
