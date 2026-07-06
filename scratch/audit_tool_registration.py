"""Assert the fleet's strict tool-access boundary."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents import brutal_vc_analyst, market_risk_quant, master_liaison
from tools import write_pitch_deck


assert brutal_vc_analyst.tools == []
assert market_risk_quant.tools == []
assert master_liaison.tools == [write_pitch_deck]
assert master_liaison.output_schema is None
print("Tool registration audit passed.")
