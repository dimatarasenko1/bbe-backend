from utils import gpt_interactor
from models.quiz import Category
import json


CATEGORIES = [
    "sports",
    "music",
    "film",
    "science",
    "history",
    "books",
    "arts",
    "games",
    "other",
]


def system_message():
    m = """You are a smart and fun quizz gamemaster. 
    With your help I am creating personalised quiz games for users to enjoy.
    The goal is to create an engaging quizz game so people can test their knowledge, learn something new and have fun.
    The idea of our quizz is that the user can decide the topic themselves and we then create a unique quizz just for them."""

    return m


def category_one_shot_prompt(quiz_title: str) -> str:
    p = f"""
    Help me categorize this quiz based on its title.

    QUIZ TITLE: {quiz_title}

    AVAILABLE CATEGORIES: {", ".join(CATEGORIES)}

    --- Instructions ---
    1. Choose the category that best fits the quiz title.
    2. Assign an emoji that best fits the quiz title.
    3. Use only the available categories provided by me.
    4. Use any emoji that exists in the regular unicode emoji list, return the emoji in Unicode format.

    --- Response Format ---
    Return a JSON object like:
    {{
      "category": "category",
      "emoji_unicode": "emojiUnicode"
    }}
    """

    return p


def is_valid_emoji(emoji: str) -> bool:
    try:
        emoji_keys = {}
        with open("data/emoji-keys.json", "r") as f:
            emoji_keys = json.load(f)

        if emoji_keys.get(emoji) is not None:
            return True

        emoji_list = []
        with open("data/full-emoji-list.json", "r") as f:
            emoji_list = json.load(f)

        for item in emoji_list:
            if emoji == item["emoji"] or emoji == item["code"]:
                return True

    except Exception as e:
        print(f"Error: {e}")
        return False

    return False


def assign_category(quiz_title: str) -> Category:
    try:
        prompt = (
            category_one_shot_prompt(quiz_title)
            .strip()
            .replace("\n\n", "\n")
            .replace("  ", " ")
        )
        response, _cost = gpt_interactor.json_gpt(prompt, system_message())

        cat = response["category"].strip().lower()
        if cat not in CATEGORIES:
            cat = "other"

        emoji = response["emoji_unicode"].strip().lower()
        if not is_valid_emoji(emoji):
            emoji = None

        return Category(slug=cat, emojiUnicode=emoji)
    except:
        return Category(slug="other", emojiUnicode=None)
