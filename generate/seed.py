import json
from utils import gpt_interactor, supa_interactor
import generate

try:
    from .categorizer import is_valid_emoji
except:
    from categorizer import is_valid_emoji

from models.quiz import DraftOption, SupaQuiz, Question
import random
import generate.final as generate_final
from datetime import datetime

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

# SAVE MOCK QUIZZES TO FIRESTORE ##


def generate_seed(option: DraftOption, category: str) -> SupaQuiz:
    prompt = (
        generate_final.final_prompt(option, category)
        .strip()
        .replace("\n\n", "\n")
        .replace("  ", " ")
    )
    response, _cost = gpt_interactor.json_gpt(
        prompt, generate_final.system_message(), temp=0.7
    )
    qs = response["questions"]

    questions = []
    for q in qs:
        stripped_answers = [
            generate_final.check_for_position_identifier(answer)
            for answer in q["answers"]
        ]
        filtered_answers, correct_index = generate_final.ensure_four_answers(
            stripped_answers, int(q["correct"]) - 1
        )
        shuffled_answers, new_correct_index = generate_final.shuffle_answers(
            filtered_answers, correct_index
        )
        questions.append(
            Question(
                question=q["question"],
                answers=shuffled_answers,
                correctIndex=new_correct_index,
            )
        )

    q1 = questions[0]
    rest = questions[1:]

    ts = datetime.now()

    quiz = SupaQuiz(
        title=option.title,
        intro=q1.question,
        category=category,
        questions=rest,
        user_id=option.user_id,
        play_count=random.randint(0, 100),
        seed=True,
        username="User",
        created_at=ts,
        updated_at=ts,
    )
    return quiz


quizzes = {}
with open("data/mock_quizzes.json", "r") as f:
    quizzes = json.load(f)

# restart --
# for key in quizzes.keys():
#     for quiz in quizzes[key]:
#         quiz["saved"] = False

# with open("data/mock_quizzes.json", "w") as f:
#     json.dump(quizzes, f, indent=4)

for category in quizzes.keys():
    for quiz in quizzes[category]:
        if quiz["saved"]:
            continue
        option = DraftOption(title=quiz["title"], user_id=None, example_question=None)
        quizz = generate_seed(option, category)
        quizz.emoji = quiz["emoji"] if quiz["emoji"] else None
        supa_interactor.save_quiz(quizz)
        quiz["saved"] = True
        with open(f"data/mock_quizzes.json", "w") as f:
            json.dump(quizzes, f, indent=4)

## END SAVE MOCK QUIZZES TO FIRESTORE ##
