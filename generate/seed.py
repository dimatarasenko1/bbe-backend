import json
from utils import gpt_interactor
import random
import re
from .categorizer import is_valid_emoji
from datetime import datetime
from models.quiz import MockQuizDetails, Question, QuizDetails
from utils import firebase_interactor


# generate a bunch of usernames
# generate a bunch of quizz ideas across different categories
# generate quizz titles and emojis for all ideas
# save them all as Mock quizz in firestore with random username and play count

## USERNAMES ##
# # Function to split username on the first underscore or second capital letter
# def split_username(username):
#     # Check for an underscore
#     if "_" in username:
#         return username.split("_", 1)

#     # Check for the second capital letter
#     capitals = [m.start() for m in re.finditer(r"[A-Z]", username)]
#     if len(capitals) > 1:
#         split_pos = capitals[1]
#         return username[:split_pos], username[split_pos:]

#     # Default case: return the username as is if no split criteria is met
#     return username, ""


# def extract_numbers(username):
#     return "".join(filter(str.isdigit, username))


# def random_transform(username):
#     only_letters = "".join(filter(lambda x: not x.isdigit(), username))
#     p1, p2 = split_username(only_letters)
#     x = extract_numbers(username)

#     transformations = [
#         lambda p1, p2, x: f"{p1.lower()}_{p2.lower()}{x}",
#         lambda p1, p2, x: f"{p1.capitalize()}{p2.lower()}{x}",
#         lambda p1, p2, x: f"{p1}{p2}{x}",
#     ]
#     return random.choice(transformations)(p1, p2, x)


# def generate_usernames(n: int):
#     p = f"""
#     -- Instructions ---
#     * Generate {n} random usernames for my game for testing purposes.

#     -- Requirements ---
#     1. Usernames should be a mix of 1) fun game nicknames users might assign themselves, 2) usernames that include first names.
#     2. All usernames should be unique.
#     3. Usernames should be between 5-12 characters long.
#     4. Use random combinations of letters, numbers and underscores. Usernames should not include any special characters.
#     5. Be creative - the usernames should not feel cliche. Think about what real people would use as usernames in a fun game.

#     Response Format:
#     A JSON array like:
#     {{"usernames": ["username1", "username2", "username3", ..., "username{n}"]}}
#     """

#     response, _cost = gpt_interactor.json_gpt(p, temp=1)

#     usernames = response["usernames"]

#     # post-process usernames
#     usernames = list(set([u.strip().replace(" ", "_") for u in usernames]))
#     usernames = [random_transform(username) for username in usernames]

#     # save usernames array to file data/usernames.json
#     with open("data/usernames.json", "w") as f:
#         json.dump(usernames, f, indent=4)


# def sample_usernames(n: int):
#     # sample n usernames at random from txt file data/usernames_dataset.txt, writh them to usernames.json
#     usernames = []
#     with open("data/usernames_dataset.txt", "r") as f:
#         usernames = f.readlines()
#         usernames = random.sample(usernames, n)
#         usernames = [u.strip() for u in usernames]

#     with open("data/usernames.json", "w") as f:
#         json.dump(usernames, f, indent=4)


# sample_usernames(200)
## END USERNAMES ##

# ## QUIZZ IDEAS ##
# categories = ["sports", "music", "film", "science", "history", "books", "arts"]


# def generate_quizz_ideas(n: int, category: str = None):
#     if category:
#         c = f"Only generate ideas that relate to the following category - {category.upper()}."
#     else:
#         c = f"Only generate ideas that don't relate to any of the following categories - {', '.join(categories).upper()}. I need niche ideas outside of these categories."

#     m = """You are a smart and fun quizz gamemaster.
#     With your help I am creating personalised quiz games for users to enjoy.
#     The goal is to create engaging quizz games so people can test their knowledge, learn something new and have fun.
#     The idea of our quizz is that the user can decide the topic themselves and we then create a unique quizz just for them."""

#     p = f"""
#     -- Instructions --
#     1. Generate {n} quizz ideas for me to give to users as examples of what they can create.
#     - {c}
#     2. Each idea should be unique, be as creative as possible and never repeat similar ideas.
#     3. The ideas should make for fun quizzes testing knowledge on a specific topic.
#     4. The ideas should be presented as a user's answer to the question "What would you like a quizz about?"
#     5. Users won't use punctuation or correct sentence grammar in their answers, so don't include any in the ideas. Just get straight to the point.

#     -- Response Format --
#     Return a JSON object like:
#     {{
#       "quizz_ideas": ["idea1", "idea2", "idea3", ..., "idea{n}"]
#     }}
#     """

#     response, _cost = gpt_interactor.json_gpt(p, system_message=m, temp=1)

#     quizz_ideas = response["quizz_ideas"]

#     # append quiz ideas to file data/quizz_ideas.json with category as key
#     with open("data/quizz_ideas.json", "r") as f:
#         data = json.load(f)

#     if category:
#         data[category] = quizz_ideas
#     else:
#         data["other"] = quizz_ideas

#     with open("data/quizz_ideas.json", "w") as f:
#         json.dump(data, f, indent=4)


# # for cat in categories:
# #     generate_quizz_ideas(70, cat)

# generate_quizz_ideas(70, "videogames")
# ## END QUIZZ IDEAS ###


## QUIZZ TITLES AND EMOJIS ##
# def generate_quiz_titles_and_emojis(quizz_idea: str):
#     sm = """You are a smart and fun quizz gamemaster.
#     With your help I am creating personalised quiz games for users to enjoy.
#     The goal is to create an engaging quizz game so people can test their knowledge, learn something new and have fun.
#     The idea of our quizz is that the user can decide the topic themselves and we then create a unique quizz just for them."""

#     p = f"""
#     Let's get started by turning the user's input into fun a quizz idea.
#     Here is the user's answer to the question "what do you want a quiz about?":
#     USER ANSWER: {quizz_idea}

#      --- Instructions ---
#     1. Generate a unique quiz idea based on the user's input.
#     2. The quiz idea should come with a catchy title and an emoji that best fits the title.

#      -- Guidelines --
#     1. The title needs to be short and clearly indicate the idea of the quiz. Make it catchy, but do not use clickbait titles or cliches.
#     2. Use any emoji that exists in the regular unicode emoji list, return the emoji in Unicode format.

#     --- Response Format ---
#     Return a JSON object like:
#     {{
#       "title": "title",
#       "emoji_unicode": "emoji_unicode"
#     }}
#     """
#     response, _cost = gpt_interactor.json_gpt(p, sm)

#     title = response["title"]
#     emoji = response["emoji_unicode"].strip().lower()
#     if not is_valid_emoji(emoji):
#         emoji = None

#     return {"title": title, "emoji": emoji}


# ideas = {}
# with open("data/quizz_ideas.json", "r") as f:
#     ideas = json.load(f)

# quizzes = {}
# with open("data/mock_quizzes.json", "r") as f:
#     quizzes = json.load(f)

# for key in ideas.keys():
#     print(f"Generating titles and emojis for {key} ideas")
#     # Only process new ideas
#     for idea in ideas[key][len(quizzes[key]) :]:
#         quizzes[key].append(generate_quiz_titles_and_emojis(idea))
#         with open(f"data/mock_quizzes.json", "w") as f:
#             json.dump(quizzes, f, indent=4)

## END QUIZZ TITLES AND EMOJIS ##

## SAVE MOCK QUIZZES TO FIRESTORE ##
# wipe_quizzes()
# usernames = []
# with open("data/usernames.json", "r") as f:
#     usernames = json.load(f)

# quizzes = {}
# with open("data/mock_quizzes.json", "r") as f:
#     quizzes = json.load(f)

# for key in quizzes.keys():
#     for quiz in quizzes[key]:
#         if quiz.get("saved"):
#             continue
#         mock_quiz = MockQuizDetails(
#             title=quiz["title"],
#             emoji=quiz["emoji"],
#             category=key,
#             play_count=random.randint(0, 100),
#             username=random.choice(usernames),
#             created_at=int(datetime.now().timestamp()),
#             seed=True,
#         )
#         # save to firestore
#         firebase_interactor.save_quizz(mock_quiz)
#         quiz["saved"] = True
#         with open(f"data/mock_quizzes.json", "w") as f:
#             json.dump(quizzes, f, indent=4)

## END SAVE MOCK QUIZZES TO FIRESTORE ##


## POPULATE QUIZZES AT RUNTIME ##
def system_message():
    m = """You are a smart and fun quizz gamemaster. 
    With your help I am creating personalised quiz games for users to enjoy.
    The goal is to create an engaging quizz game so people can test their knowledge, learn something new and have fun.
    The idea of our quizz is that the user can decide the topic themselves and we then create a unique quizz just for them."""

    return m


def one_shot_populate_prompt(mock_quizz: MockQuizDetails) -> str:
    p = f"""
    The user has chosen a quiz idea that we now need to fill out with questions and answers. 
    Here is the user's chosen quiz idea:
    Title: {mock_quizz.title}

    --- Instructions ---
    1. Generate 20 multiple choice questions for the quiz.
    2. Each question should have 4 answer choices with one correct answer.
    3. The questions should only relate to the topic of the quiz.
    5. The questions should get harder as the quiz progresses. Only a real expert should be able to answer the last question.

    -- Guidelines --
    1. IMPORTANT: Do not cover questions where you are not certain about the answer.
    2. The correct answer should be clear and not misleading.
    3. The tone of voice for each question should be casual, fun and engaging. 
    4. Be creative with the questions, don't just use the same structure for each question and cover various aspects of the quiz topic.
    5. It is all about creating a fun and engaging quiz that the user will enjoy playing.

    --- Quiz Example ---
    Title: "Space Exploration: The Final Frontier"
    Intro: "Embark on a journey through the cosmos and discover the wonders of space exploration."
    Example Question: "Which spacecraft was the first to land on Mars?"

    Question 1: "What is the name of the first artificial satellite launched into space?"
    Answer Choices: A) Luna 1, B) Sputnik 1, C) Explorer 1, D) Vanguard 1
    Correct Answer: B

    Question 2: "Who was the first human to travel into space?"
    Answer Choices: A) Yuri Gagarin, B) Alan Shepard, C) John Glenn, D) Neil Armstrong
    Correct Answer: A

    Question 3: "Which year did the first dog orbit the Earth?"
    Answer Choices: A) 1957, B) 1959, C) 1961, D) 1963
    Correct Answer: A

    Question 4: "Which mission was the first to successfully land humans on the Moon?"
    Answer Choices: A) Apollo 8, B) Apollo 10, C) Apollo 11, D) Apollo 13
    Correct Answer: C

    Question 5: "Which mission resulted in a famous disaster during launch?"
    Answer Choices: A) Challenger, B) Discovery, C) Atlantis, D) Columbia
    Correct Answer: A

    Question 6: "What is the line separating Earth's atmosphere from outer space called?"
    Answer Choices: A) Karman Line, B) Armstrong Line, C) Exobase, D) Tropopause
    Correct Answer: A

    Question 7: "How many countries are part of the International Space Station program?"
    Answer Choices: A) 10, B) 15, C) 20, D) 25
    Correct Answer: C

    Question 8: "What was the first spacecraft to fly by Pluto?"
    Answer Choices: A) New Horizons, B) Voyager 1, C) Cassini, D) Galileo
    Correct Answer: A

    Question 9: "How many people have walked on the Moon?"
    Answer Choices: A) 8, B) 10, C) 12, D) 14
    Correct Answer: C
    
    Question 10: "What is the average temperature on the surface of Mars?"
    Answer Choices: A) -60°C, B) -80°C, C) 0°C, D) -40°C
    Correct Answer: A
    
    --- Response Format ---
    Return a JSON object of the final quizz like:
    {{
      "questions": [
        {{
            "question": "question 1",
            "answers": ["answer1", "answer2", "answer3", "answer4"],
            "correct": between 1-4
        }},
        {{
            "question": "question 2",
            "answers": ["answer1", "answer2", "answer3", "answer4"],
            "correct": between 1-4
        }}
        ...
      ]
    }}
"""

    return p


def populate_quizz(mock_quizz: MockQuizDetails):
    prompt = (
        one_shot_populate_prompt(mock_quizz)
        .strip()
        .replace("\n\n", "\n")
        .replace("  ", " ")
    )
    response, _cost = gpt_interactor.json_gpt(prompt, system_message())
    qs = response["questions"]

    example_question = qs[-1]["question"]

    questions = [
        Question(
            question=q["question"],
            answers=q["answers"],
            correctIndex=int(q["correct"]) - 1,
        )
        for q in qs[:-1]
    ]

    questions = questions[:20]
    first_ten = questions[::2]
    rest = questions[1::2]
    final_questions = first_ten + rest

    full_quiz = QuizDetails(
        intro=example_question,
        questions=final_questions,
        **mock_quizz.model_dump(),
    )
    full_quiz.populated = True
    return full_quiz
