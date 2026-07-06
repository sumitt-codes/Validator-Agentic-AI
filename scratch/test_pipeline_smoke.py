"""Explicit live API smoke test for the original Pune validator scenario."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import run_pipeline


PUNE_EV_BIKE_IDEA = (
    "A luxury EV bike rental app in Pune targeting corporate commuters "
    "with a premium subscription layer."
)


if __name__ == "__main__":
    asyncio.run(run_pipeline(PUNE_EV_BIKE_IDEA))
