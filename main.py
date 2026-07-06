"""Interactively load the sample report or run the live validator pipeline."""

import asyncio
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents import brutal_vc_analyst, market_risk_quant, master_liaison
from schemas import FinalValidationPayload, MarketRiskAnalysis, StartupBlueprint
from tools import parse_agent_response


load_dotenv()

WORKSPACE_ROOT = Path(__file__).resolve().parent
SESSION_OUTPUT_PATH = WORKSPACE_ROOT / "session_output.json"
INDEX_PATH = WORKSPACE_ROOT / "index.html"
SAMPLE_INDEX_PATH = WORKSPACE_ROOT / "fixtures" / "sample_index.html"
SAMPLE_SESSION_OUTPUT_PATH = (
    WORKSPACE_ROOT / "fixtures" / "sample_session_output.json"
)
APP_NAME = "startup_validator"
USER_ID = "autonomous_pipeline"


def utc_timestamp() -> str:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def persist(data: dict[str, Any]) -> None:
    """Atomically replace the local JSON session snapshot."""
    temporary_path = SESSION_OUTPUT_PATH.with_suffix(".json.tmp")
    temporary_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temporary_path.replace(SESSION_OUTPUT_PATH)


async def run_agent(
    *,
    agent: Any,
    session_id: str,
    state: dict[str, Any],
    message: str,
) -> str | dict[str, Any]:
    """Run one agent in its own runner and in-memory session service."""
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
        state=state,
    )
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    events = [
        event
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=message)],
            ),
        )
    ]
    return parse_agent_response(events)


async def run_pipeline(idea: str) -> FinalValidationPayload:
    """Execute all three agents and return the validated combined payload."""
    session_id = str(uuid4())
    snapshot: dict[str, Any] = {"raw_idea": idea, "timestamp": utc_timestamp()}

    print("1/3  Brutal VC analyst")
    blueprint_response = await run_agent(
        agent=brutal_vc_analyst,
        session_id=session_id,
        state={},
        message=idea,
    )
    blueprint = StartupBlueprint.model_validate(blueprint_response)
    snapshot["blueprint"] = blueprint.model_dump()
    persist(snapshot)

    print("2/3  Market risk quant")
    market_response = await run_agent(
        agent=market_risk_quant,
        session_id=session_id,
        state={"idea": idea, "blueprint": blueprint.model_dump_json()},
        message="Complete the market-risk assessment from the supplied session state.",
    )
    market_risk = MarketRiskAnalysis.model_validate(market_response)
    snapshot["market_risk"] = market_risk.model_dump()
    persist(snapshot)

    print("3/3  Master liaison")
    INDEX_PATH.unlink(missing_ok=True)
    conclusion_response = await run_agent(
        agent=master_liaison,
        session_id=session_id,
        state={
            "idea": idea,
            "blueprint": blueprint.model_dump_json(),
            "market_risk": market_risk.model_dump_json(),
        },
        message="Create the final investor report and return its conclusion.",
    )
    if not isinstance(conclusion_response, str):
        raise TypeError("Master liaison must return conclusion_text as plain text")
    if not INDEX_PATH.is_file() or INDEX_PATH.stat().st_size == 0:
        raise RuntimeError("Master liaison did not generate index.html")

    payload = FinalValidationPayload(
        idea=idea,
        blueprint=blueprint,
        market_risk=market_risk,
        conclusion_text=conclusion_response.strip(),
    )
    persist(
        {
            "raw_idea": idea,
            "blueprint": blueprint.model_dump(),
            "market_risk": market_risk.model_dump(),
            "conclusion_text": conclusion_response.strip(),
            "timestamp": utc_timestamp(),
        }
    )
    print(f"Complete: {SESSION_OUTPUT_PATH} and {INDEX_PATH}")
    return payload


def load_sample_report() -> bool:
    """Restore the checked-in sample artifacts without contacting Gemini."""
    try:
        shutil.copyfile(SAMPLE_INDEX_PATH, INDEX_PATH)
        shutil.copyfile(SAMPLE_SESSION_OUTPUT_PATH, SESSION_OUTPUT_PATH)
    except FileNotFoundError:
        print(
            "Sample fixtures not found — run the pipeline once with a real idea "
            "first to generate them."
        )
        return False
    return True


if __name__ == "__main__":
    raw_idea = input(
        "Enter your startup idea (or press Enter to see a sample report for "
        "a Pune EV bike rental idea): "
    ).strip()

    if raw_idea == "":
        if load_sample_report():
            print(
                "Loaded sample report (no API calls made). Open index.html or "
                "refresh the dashboard to view it."
            )
    else:
        asyncio.run(run_pipeline(raw_idea))
