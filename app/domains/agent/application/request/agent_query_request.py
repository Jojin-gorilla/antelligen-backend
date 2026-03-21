from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class RiskLevel(str, Enum):
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"


class InvestmentHorizon(str, Enum):
    SHORT = "short"
    MID = "mid"
    LONG = "long"


class UserProfileRequest(BaseModel):
    risk_level: RiskLevel
    investment_horizon: InvestmentHorizon


class QueryOptionsRequest(BaseModel):
    agents: Optional[list[str]] = None
    max_tokens: Optional[int] = 1024

    @field_validator("agents")
    @classmethod
    def validate_agents(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return v

        allowed = {"stock", "news", "finance", "disclosure"}
        for agent in v:
            if agent not in allowed:
                raise ValueError(
                    f"Unsupported agent: {agent}. "
                    f"Allowed agents: {', '.join(sorted(allowed))}"
                )
        return v

    @field_validator("max_tokens")
    @classmethod
    def validate_max_tokens(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 1 or v > 4096):
            raise ValueError("max_tokens must be between 1 and 4096")
        return v


class AgentQueryRequest(BaseModel):
    query: str
    ticker: Optional[str] = None
    session_id: Optional[str] = None
    user_profile: Optional[UserProfileRequest] = None
    options: Optional[QueryOptionsRequest] = None

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("query must not be empty")
        return v.strip()

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v

        value = v.strip()
        if not value:
            raise ValueError("ticker must not be empty")
        return value
