from utils import gpt_interactor
from models.quiz import DraftOption, DraftInput


def system_message():
    m = """You are a smart and fun quizz gamemaster. 
    With your help I am creating personalised quiz games for users to enjoy.
    The goal is to create an engaging quizz game so people can test their knowledge, learn something new and have fun.
    The idea of our quizz is that the user can decide the topic themselves and we then create a unique quizz just for them."""

    return m


def two_shot_draft_prompt(user_input: str):
    p = f"""
    Let's get started by turning the user's input into fun quizz ideas. 
    Here is the user's answer to the question "what do you want a quiz about?":
    USER ANSWER: {user_input}

    --- Instructions ---
    1. Generate two unique and different quiz ideas based on the user's input.
    2. Each quiz idea should have a title and an example question.
    3. IMPORTANT: The two ideas should be very different from each other. Take a second to be creative and make sure the two quizzes you generate are not too similar.

    -- Guidelines --
    1. The title needs to be short and clearly indicate the idea of the quiz. Make it catchy, but do not use clickbait titles or cliches.
    3. The example question should be interesting and engaging. It should be challenging enough to make the user want to play the quiz.

    --- Quiz Examples ---
    User input: "space exploration"

    Quiz 1:
    Title: "Space Exploration: Humanity's Journey Beyond Earth"
    Example Question: "Which spacecraft was the first to land on Mars?"

    Quiz 2:
    Title: "How well do you know the Milky Way?"
    Example Question: "How many light years across is the Milky Way?"
    
    --- Response Format ---
    Return a JSON object of quizz suggestions like:
    {{
      "quizzes":
      [
        {{
            "title": "title",
            "example_question": "example_question"
        }},
        {{
            "title": "title",
            "example_question": "example_question"
        }}
      ]
    }}
    """
    return p


def generate_draft(payload: DraftInput):
    prompt = (
        two_shot_draft_prompt(payload.user_input)
        .strip()
        .replace("\n\n", "\n")
        .replace("  ", " ")
    )
    response, _cost = gpt_interactor.json_gpt(prompt, system_message())
    options = [
        DraftOption(
            title=option["title"],
            example_question=option["example_question"],
            user_id=payload.user_id,
        )
        for option in response["quizzes"]
    ]
    return options
