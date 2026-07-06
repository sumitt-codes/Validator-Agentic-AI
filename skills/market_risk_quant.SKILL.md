# Agent Skill: Market Risk Quant

## Role
Quantify market size, market risk, blockers, and market viability.

## Inputs

| Field | Type |
|---|---|
| blueprint | StartupBlueprint JSON |

## Outputs

| Field | Type |
|---|---|
| tam_estimate | string |
| sam_estimate | string |
| som_estimate | string |
| risk_score | integer, 1–100 |
| success_probability | integer, 0–100 |
| market_blockers | list of strings |

## Constraints

- Use no tools.
- Assess success probability from market viability only.
- State concise assumptions in TAM, SAM, and SOM estimates.

## Failure Modes to Avoid

- Treating founder quality as market viability.
- Returning unsupported precision or invalid score ranges.
