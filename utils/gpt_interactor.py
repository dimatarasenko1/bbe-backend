from openai import OpenAI
import json
import tiktoken as tiktoken
import logging
from config import settings
from typing import List


def count_tokens(text: str) -> int:
    estimate = len(tiktoken.encoding_for_model("gpt-4").encode(text))
    return int(estimate * 1.3)


def estimate_cost(text: str, input: bool) -> float:
    price_per_million = 5.00 if input else 15.00
    token_count = count_tokens(text)
    return (token_count / 1_000_000) * price_per_million


def json_gpt(
    prompt: str,
    system_message: str = "",
    message_history: List[dict] = [],
    max_tokens: int = 4096,
    temp: float = 0.8,
    model: str = "gpt-4o",
) -> dict:

    if not system_message:
        system_message = "You are my helpful assistant."

    messages = [{"role": "system", "content": system_message}]

    if message_history:
        messages.extend(message_history)
    messages.append({"role": "user", "content": prompt})

    client = OpenAI(
        api_key=settings.OPENAI_KEY,
    )

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
        max_tokens=max_tokens,
        temperature=temp,
    )

    response_text = completion.choices[0].message.content
    parsed = json.loads(response_text)

    logging.info(f"[GPT Response] Response: {parsed}")

    # Cost
    input_cost = estimate_cost(prompt, True)
    output_cost = estimate_cost(response_text, False)
    total_cost = input_cost + output_cost

    logging.info(f"[GPT] Cost: {total_cost:.4f}")

    return parsed, total_cost


def moderation_check(user_text: str) -> bool:
    client = OpenAI(
        api_key=settings.OPENAI_KEY,
    )
    response = client.moderations.create(input=user_text)
    flagged = response.results[0].flagged
    if flagged:
        raise Exception(f"[GPT] Moderation Error. Text not allowed: {user_text}")
    return flagged == False
