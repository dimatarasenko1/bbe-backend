from models.quiz import DraftOption, QuizDetails, Question
from utils import gpt_interactor
from datetime import datetime


def system_message():
    m = """You are a smart and fun quizz gamemaster. 
    With your help I am creating personalised quiz games for users to enjoy.
    The goal is to create an engaging quizz game so people can test their knowledge, learn something new and have fun.
    The idea of our quizz is that the user can decide the topic themselves and we then create a unique quizz just for them."""

    return m


def two_shot_final_prompt(draft: DraftOption) -> str:
    p = f"""
    The user has chosen a quiz idea that we now need to fill out with questions and answers. 
    Here is the user's chosen quiz idea:
    Title: {draft.title}
    Example Question: {draft.example_question}

    --- Instructions ---
    1. Generate 20 multiple choice questions for the quiz.
    2. Each question should have 4 answer choices with one correct answer.
    3. The questions should only relate to the topic of the quiz.
    4. The example question should not be included.
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


def generate_final(draft: DraftOption, username: str) -> QuizDetails:
    prompt = (
        two_shot_final_prompt(draft).strip().replace("\n\n", "\n").replace("  ", " ")
    )
    response, _cost = gpt_interactor.json_gpt(prompt, system_message())
    qs = response["questions"]

    questions = [
        Question(
            question=q["question"],
            answers=q["answers"],
            correctIndex=int(q["correct"]) - 1,
        )
        for q in qs
    ]

    # play around with the order a bit
    questions = questions[:20]
    first_ten = questions[::2]
    rest = questions[1::2]
    final_questions = first_ten + rest

    quiz = QuizDetails(
        title=draft.title,
        intro=draft.example_question,
        questions=final_questions,
        username=username,
        created_at=int(datetime.now().timestamp()),
    )
    return quiz
