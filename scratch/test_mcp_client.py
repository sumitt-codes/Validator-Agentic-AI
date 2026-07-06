"""End-to-end stdio client test for the standalone MCP tool."""

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from schemas import MarketRiskAnalysis


async def main() -> None:
    workspace = Path(__file__).resolve().parents[1]
    server = StdioServerParameters(
        command=sys.executable,
        args=[str(workspace / "mcp_server.py")],
        cwd=str(workspace),
    )
    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(
                "analyze_market_risk",
                arguments={
                    "idea_text": (
                        "A subscription cold-chain delivery network for independent "
                        "pharmacies in tier-two Indian cities."
                    ),
                    "blueprint": {
                        "industry": "HealthTech / Logistics",
                        "complexity_tier": "High",
                        "immediate_competitors": ["Snowman Logistics", "ColdEX"],
                        "brutal_premise_flaw": (
                            "Low order density can make temperature-controlled "
                            "last-mile economics structurally unworkable."
                        ),
                    },
                },
            )
            if result.isError:
                raise AssertionError(f"MCP tool failed: {result.content}")
            structured = result.structuredContent
            if structured and "result" in structured:
                structured = structured["result"]
            if not structured:
                text = next(
                    item.text for item in result.content if hasattr(item, "text")
                )
                structured = json.loads(text)
            MarketRiskAnalysis.model_validate(structured)
            print("MCP client validation passed.")


if __name__ == "__main__":
    asyncio.run(main())
