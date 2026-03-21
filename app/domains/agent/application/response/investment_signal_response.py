from enum import Enum

from pydantic import BaseModel, field_validator


class InvestmentSignal(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class InvestmentSignalResponse(BaseModel):
    agent_name: str
    ticker: str
    signal: InvestmentSignal
    confidence: float
    summary: str
    key_points: list[str]

    @field_validator("agent_name")
    @classmethod
    def validate_agent_name(cls, v: str) -> str:
        allowed = {"news", "finance", "disclosure"}
        if v not in allowed:
            raise ValueError(
                f"Unsupported agent: {v}. "
                f"Allowed agents: {', '.join(sorted(allowed))}"
            )
        return v

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        if v < 0.0 or v > 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        return round(v, 4)

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("ticker must not be empty")
        return v.strip()

    @field_validator("key_points")
    @classmethod
    def validate_key_points(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("key_points must contain at least one item")
        return v
