"""Resilient LLM invocation helper with Pydantic output validation and automated retry."""

import json
import logging
import os
from pathlib import Path
from typing import Callable, Type, TypeVar

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, ValidationError

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

_client: Groq | None = None


def get_groq_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client


def call_llm_with_validation(
    schema: Type[T],
    prompt: str,
    system_prompt: str = "Return only valid JSON matching the requested schema.",
    pre_validate_hook: Callable[[dict], dict] | None = None,
    model: str | None = None,
    temperature: float = 0.0,
    max_retries: int = 1,
) -> T:
    """Call Groq LLM with strict Pydantic validation and one corrective retry on failure."""
    client = get_groq_client()
    model_name = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    last_error: Exception | None = None
    raw_content = ""

    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=temperature,
            )
            raw_content = response.choices[0].message.content or "{}"
            parsed_json = json.loads(raw_content)

            if pre_validate_hook:
                parsed_json = pre_validate_hook(parsed_json)

            # Validate against Pydantic schema
            validated_model = schema.model_validate(parsed_json)
            return validated_model

        except (json.JSONDecodeError, ValidationError) as err:
            last_error = err
            logger.warning(
                "LLM validation failed (attempt %d/%d): %s",
                attempt + 1,
                max_retries + 1,
                err,
            )

            if attempt < max_retries:
                # Append error message as corrective feedback for retry
                messages.append({"role": "assistant", "content": raw_content})
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            f"Your previous response failed Pydantic schema validation with error:\n{err}\n\n"
                            f"Please fix the fields, ensure all required fields are present with correct types, "
                            f"and output only valid JSON matching the schema."
                        ),
                    }
                )

    raise ValueError(
        f"LLM output failed validation after {max_retries + 1} attempts: {last_error}"
    )
