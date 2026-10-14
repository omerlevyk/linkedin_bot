from __future__ import annotations

from datetime import date

from .config import Config
from .http import ApiError, post_json


FORMATS = (
    "an educational explanation with one practical example",
    "a surprising 'Did you know?' fact followed by why it matters",
    "a short technical riddle; invite readers to answer before revealing the answer near the end",
    "a practical career lesson for someone becoming a DevOps or MLOps engineer",
    "a realistic production mistake and the lesson learned",
    "a concise comparison of two approaches, including when to use each",
    "a useful checklist readers can apply today",
)


def choose_subject(config: Config, today: date) -> tuple[str, str]:
    ordinal = today.toordinal()
    return config.topics[ordinal % len(config.topics)], FORMATS[ordinal % len(FORMATS)]


def _extract_text(response: dict) -> str:
    pieces = []
    for item in response.get("output", []):
        if item.get("type") == "message":
            pieces.extend(content["text"] for content in item.get("content", [])
                          if content.get("type") == "output_text" and content.get("text"))
    text = "\n".join(pieces).strip()
    if not text:
        raise ApiError("OpenAI response did not contain output text")
    return text


def generate(config: Config, recent_previews: list[str], today: date | None = None) -> str:
    today = today or date.today()
    topic, post_format = choose_subject(config, today)
    recent = "\n".join(f"- {x}" for x in recent_previews[-10:]) or "- None yet"
    instructions = f"""You write LinkedIn posts for an experienced DevOps engineer.
Write in {config.language}. The voice is {config.tone}.
Return only the finished post, with no title label or meta-commentary.
The post must be at most {config.max_chars} characters.
Start with a strong, natural hook. Use short paragraphs and concrete technical details.
End with one genuine discussion question. Use at most 3 relevant hashtags.
Do not invent statistics, incidents, benchmarks, quotations, or product behavior.
Avoid engagement bait, hype, fake personal experiences, and guaranteed outcomes.
Make the content useful, technically correct, and understandable on its own."""
    prompt = f"""Create today's post.

Topic: {topic}
Format: {post_format}
Date: {today.isoformat()}

Avoid repeating these recent posts:
{recent}"""
    response, _ = post_json(
        "https://api.openai.com/v1/responses",
        {"model": config.openai_model, "instructions": instructions, "input": prompt},
        {"Authorization": f"Bearer {config.openai_api_key}"},
    )
    post = _extract_text(response)
    if len(post) > config.max_chars:
        raise ValueError(f"Generated post is {len(post)} characters; maximum is {config.max_chars}")
    return post
