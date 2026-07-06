"""Tools and event-stream utilities for the validator fleet."""

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any


WORKSPACE_ROOT = Path(__file__).resolve().parent


def write_pitch_deck(html_content: str) -> str:
    """Write a complete standalone HTML pitch deck to the workspace index.html.

    Args:
        html_content: Full, valid HTML for the investor-facing pitch deck.

    Returns:
        A short confirmation containing the absolute output path.
    """
    output_path = WORKSPACE_ROOT / "index.html"
    output_path.write_text(html_content, encoding="utf-8")
    return f"Pitch deck written to {output_path}"


def parse_agent_response(events: Iterable[Any]) -> str | dict[str, Any]:
    """Extract the final text or JSON object from an ADK runner event stream.

    Args:
        events: Materialized events yielded by ``Runner.run_async``.

    Returns:
        A decoded JSON object when the final response is a JSON object,
        otherwise the final response text.

    Raises:
        ValueError: If the stream has no textual model response.
    """
    final_chunks: list[str] = []
    all_chunks: list[str] = []

    for event in events:
        content = getattr(event, "content", None)
        parts = getattr(content, "parts", None) or []
        chunks = [
            part.text
            for part in parts
            if isinstance(getattr(part, "text", None), str) and part.text
        ]
        all_chunks.extend(chunks)
        is_final = getattr(event, "is_final_response", None)
        if callable(is_final) and is_final():
            final_chunks = chunks

    text = "".join(final_chunks or all_chunks).strip()
    if not text:
        raise ValueError("Agent event stream contained no textual response")

    try:
        decoded = json.loads(text)
    except json.JSONDecodeError:
        return text
    return decoded if isinstance(decoded, dict) else text
