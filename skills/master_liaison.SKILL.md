# Agent Skill: Master Liaison

## Role
Synthesize the analyses, write the investor HTML report, and return its verdict.

## Inputs

| Field | Type |
|---|---|
| blueprint | StartupBlueprint JSON |
| market_risk | MarketRiskAnalysis JSON |

## Outputs

| Field | Type |
|---|---|
| index.html | standalone HTML document |
| conclusion_text | plain-text paragraph |

## Constraints

- Use only `write_pitch_deck`.
- Do not use an output schema.
- Reply with only the conclusion paragraph after writing the report.
- Keep the validator conclusion in its isolated, removable section.

## Failure Modes to Avoid

- Returning JSON or HTML as the final text response.
- Omitting the success badge or calling the write tool more than once.
