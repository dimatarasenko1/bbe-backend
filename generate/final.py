from models.quiz import DraftOption, SupaQuiz, Question
from utils import gpt_interactor
from datetime import datetime
import random
from typing import List
import re


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
    1. Generate 15 multiple choice questions for the quiz.
    2. Each question should have 4 answer choices with one correct answer.
    3. The questions should only relate to the topic of the quiz.
    4. The quizz is for expert-level players, so the questions should be very challenging.
    5. The questions should get harder as the quiz progresses. Only a real know-it-all on the topic should be able to answer all the questions.

    -- Quiestion Guidelines --
    1. IMPORTANT: Never create questions where the answer is in the question itself. eg "Which character is famous for the line, "Bond, James Bond"?" - James Bond.
    2. IMPORTANT: Do not cover questions where you are not certain about the answer.
    3. The correct answer should be clear and not misleading.
    4. The tone of voice for each question should be casual, fun and engaging. 
    5. Be creative with the questions, don't just use the same structure for each question and cover various aspects of the quiz topic.
    6. Do NOT use position identifiers in answer options texts - e.g. 1) or A) etc. Each answer option should just be standalone text.

   --- Question Tone of Voice And Format Examples ---
    Quiz Title: "Space Exploration: The Final Frontier"

    Question: "Who was the first human to travel into space?"
    Answer Choices: A) Yuri Gagarin, B) Alan Shepard, C) John Glenn, D) Neil Armstrong

    Question: "Which year did the first dog orbit the Earth?"
    Answer Choices: A) 1957, B) 1959, C) 1961, D) 1963

    Question: "What is the line separating Earth's atmosphere from outer space called?"
    Answer Choices: A) Karman Line, B) Armstrong Line, C) Exobase, D) Tropopause
    
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


def ensure_four_answers(answers, correct_index):
    correct_answer = answers[correct_index]
    if len(answers) > 4:
        # Ensure the correct answer is included
        filtered_answers = [correct_answer] + random.sample(
            [a for a in answers if a != correct_answer], 3
        )
    else:
        filtered_answers = answers[:]

    return filtered_answers, filtered_answers.index(correct_answer)


def shuffle_answers(answers: List[str], correct_index: int):
    print(correct_index, answers)
    shuffled_answers = answers[:]
    random.shuffle(shuffled_answers)
    new_correct_index = shuffled_answers.index(answers[correct_index])
    return shuffled_answers, new_correct_index


def check_for_position_identifier(answer: str) -> str:
    # Regular expression pattern to match leading position identifiers
    pattern = r"^\s*(\d+\.\s*|\d+\)\s*|[a-zA-Z]\.\s*|[a-zA-Z]\)\s*)"
    return re.sub(pattern, "", answer)


def filter_out_example_question(
    questions: List[str], example_question: str
) -> List[str]:
    return [
        q
        for q in questions
        if q["question"].strip().lower() != example_question.strip().lower()
    ]


def generate_final(draft: DraftOption) -> SupaQuiz:
    prompt = (
        two_shot_final_prompt(draft).strip().replace("\n\n", "\n").replace("  ", " ")
    )
    response, _cost = gpt_interactor.json_gpt(prompt, system_message(), temp=0.7)
    qs = response["questions"]
    qs = filter_out_example_question(qs, draft.example_question)

    questions = []
    for q in qs:
        stripped_answers = [
            check_for_position_identifier(answer) for answer in q["answers"]
        ]
        filtered_answers, correct_index = ensure_four_answers(
            stripped_answers, int(q["correct"]) - 1
        )
        shuffled_answers, new_correct_index = shuffle_answers(
            filtered_answers, correct_index
        )
        questions.append(
            Question(
                question=q["question"],
                answers=shuffled_answers,
                correctIndex=new_correct_index,
            )
        )

    ts = datetime.now()

    quiz = SupaQuiz(
        title=draft.title,
        intro=draft.example_question,
        questions=questions,
        user_id=draft.user_id,
        username="User",
        created_at=ts,
        updated_at=ts,
    )
    return quiz
