"""Validated data contracts shared by the startup validator fleet."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class StartupBlueprint(BaseModel):
    """Agent 1's structural assessment of a startup idea."""

    industry: str
    complexity_tier: Literal["Low", "Medium", "High"]
    immediate_competitors: list[str]
    brutal_premise_flaw: str

    @field_validator("immediate_competitors")
    @classmethod
    def require_two_competitors(cls, value: list[str]) -> list[str]:
        if len(value) != 2:
            raise ValueError("immediate_competitors must contain exactly 2 items")
        return value


class MarketRiskAnalysis(BaseModel):
    """Agent 2's market-sizing and market-viability assessment."""

    tam_estimate: str
    sam_estimate: str
    som_estimate: str
    risk_score: int = Field(ge=1, le=100)
    success_probability: int = Field(ge=0, le=100)
    market_blockers: list[str]


class FinalValidationPayload(BaseModel):
    """The application-owned object assembled after all three agent runs."""

    idea: str
    blueprint: StartupBlueprint
    market_risk: MarketRiskAnalysis
    conclusion_text: str
