"""Standalone MCP server exposing only the market-risk quant agent."""

import json
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from mcp.server.fastmcp import FastMCP

from agents import market_risk_quant
from schemas import MarketRiskAnalysis, StartupBlueprint
from tools import parse_agent_response


load_dotenv()

APP_NAME = "market_risk_mcp"
USER_ID = "mcp_client"
mcp = FastMCP("Startup Validator Market Risk")


@mcp.tool()
async def analyze_market_risk(
    idea_text: str,
    blueprint: dict[str, Any],
) -> dict[str, Any]:
    """Analyze market size and viability for a startup blueprint.

    Args:
        idea_text: The original raw startup idea for market context.
        blueprint: A StartupBlueprint-shaped object from the VC analyst.

    Returns:
        A MarketRiskAnalysis-shaped JSON object.
    """
    validated_blueprint = StartupBlueprint.model_validate(blueprint)
    session_id = str(uuid4())
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
        state={
            "idea": idea_text,
            "blueprint": validated_blueprint.model_dump_json(),
        },
    )
    runner = Runner(
        agent=market_risk_quant,
        app_name=APP_NAME,
        session_service=session_service,
    )
    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
                    "Complete the market-risk assessment. Use this original idea only "
                    f"as market context: {idea_text}"
                )
            )
        ],
    )
    events = [
        event
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=message,
        )
    ]
    response = parse_agent_response(events)
    analysis = MarketRiskAnalysis.model_validate(response)
    return analysis.model_dump()


if __name__ == "__main__":
    mcp.run(transport="stdio")
