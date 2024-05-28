from utils import gpt_interactor
from models.quiz import DraftOption


def system_message():
    m = """You are a smart and witty trivia gamemaster. 
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
    1. Generate two unique quiz ideas based on the user's input.
    2. Each quiz idea should have a title, an intro and an example question.
    3. Do not generate all the questions, just one example question.
    4. The user will choose one of the two quiz ideas to continue refining.

    -- Guidelines --
    1. The tone of voice for quizz title, intro and example question should be casual, fun and engaging. 
    2. The title needs to be catchy and the intro should be intriguing.
    3. The question needs to be phrased so it can be answered in a multiple choice format. No need to generate the answer choices for the draft.
    5. If the user input is very specific, make sure to really go down that rabbit hole. The user will appreciate a specific quiz about their niche interest.
    6. If the user input is very broad, feel free to be creative and add a twist to make it more engaging.
    7. It is all about creating a fun and engaging quiz that the user will enjoy playing.

    --- Quiz Examples ---
    User input: "space exploration"

    Quiz 1:
    Title: "Space Exploration: The Final Frontier"
    Intro: "Embark on a journey through the cosmos and discover the wonders of space exploration."
    Example Question: "Which spacecraft was the first to land on Mars?"

    Quiz 2:
    Title: "The Milky Way Trivia Challenge"
    Intro: "Test your knowledge of our galaxy in this cosmic trivia adventure."
    Example Question: "How many light years across is the Milky Way?"
    
    --- Response Format ---
    Return a JSON object of quizz suggestions like:
    {{
      "quizzes":
      [
        {{
            "title": "title",
            "intro": "intro",
            "example_question": "example_question"
        }},
        {{
            "title": "title",
            "intro": "intro",
            "example_question": "example_question"
        }}
      ]
    }}
    """
    return p


def generate_draft(user_input: str):
    prompt = (
        two_shot_draft_prompt(user_input)
        .strip()
        .replace("\n\n", "\n")
        .replace("  ", " ")
    )
    response, _cost = gpt_interactor.json_gpt(prompt, system_message())
    options = [
        DraftOption(
            title=option["title"],
            intro=option["intro"],
            example_question=option["example_question"],
        )
        for option in response["quizzes"]
    ]
    return options
