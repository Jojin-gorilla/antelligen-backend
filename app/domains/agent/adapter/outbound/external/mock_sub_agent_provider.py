import random

from app.domains.agent.application.port.sub_agent_provider import SubAgentProvider
from app.domains.agent.application.response.investment_signal_response import (
    InvestmentSignalResponse,
)
from app.domains.agent.application.response.sub_agent_response import SubAgentResponse

MOCK_STOCK_DATA = {
    "005930": {
        "ticker": "005930",
        "stock_name": "Samsung Electronics",
        "market": "KOSPI",
        "current_price": 72000,
        "change_rate": -1.23,
    },
    "000660": {
        "ticker": "000660",
        "stock_name": "SK hynix",
        "market": "KOSPI",
        "current_price": 185000,
        "change_rate": 2.45,
    },
    "005380": {
        "ticker": "005380",
        "stock_name": "Hyundai Motor",
        "market": "KOSPI",
        "current_price": 248000,
        "change_rate": 0.81,
    },
    "035420": {
        "ticker": "035420",
        "stock_name": "NAVER",
        "market": "KOSPI",
        "current_price": 210000,
        "change_rate": -0.47,
    },
    "035720": {
        "ticker": "035720",
        "stock_name": "Kakao",
        "market": "KOSPI",
        "current_price": 42000,
        "change_rate": 1.20,
    },
}

MOCK_NEWS_SIGNALS: dict[str, dict] = {
    "005930": {
        "agent_name": "news",
        "ticker": "005930",
        "signal": "bullish",
        "confidence": 0.82,
        "summary": "AI semiconductor investment momentum remains positive.",
        "key_points": [
            "Additional AI chip capacity investment was announced.",
            "HBM roadmap execution remains on schedule.",
            "Broker target prices were revised upward.",
        ],
    },
    "000660": {
        "agent_name": "news",
        "ticker": "000660",
        "signal": "bullish",
        "confidence": 0.78,
        "summary": "HBM demand continues to support earnings improvement.",
        "key_points": [
            "HBM4 production line ramp-up is underway.",
            "Major supply contracts remain in place.",
        ],
    },
}

MOCK_FINANCE_SIGNALS: dict[str, dict] = {
    "005930": {
        "agent_name": "finance",
        "ticker": "005930",
        "signal": "neutral",
        "confidence": 0.55,
        "summary": "Revenue is improving, but margin recovery remains limited.",
        "key_points": [
            "Quarterly revenue growth remains positive year over year.",
            "Operating margin is still below the historical average.",
            "Semiconductor recovery is improving gradually.",
        ],
    },
    "000660": {
        "agent_name": "finance",
        "ticker": "000660",
        "signal": "bullish",
        "confidence": 0.88,
        "summary": "HBM sales growth is driving strong profitability.",
        "key_points": [
            "Operating profit remains near peak levels.",
            "HBM mix continues to expand.",
            "DRAM pricing remains supportive.",
        ],
    },
}

MOCK_DISCLOSURE_SIGNALS: dict[str, dict] = {
    "005930": {
        "agent_name": "disclosure",
        "ticker": "005930",
        "signal": "bearish",
        "confidence": 0.71,
        "summary": "Treasury stock disposal can create short-term supply pressure.",
        "key_points": [
            "Treasury stock disposal was disclosed.",
            "The disposal window spans several months.",
            "Near-term dilution concern remains.",
        ],
    },
}

DEFAULT_TICKER = "005930"
COMPANY_NAME_TO_TICKER = {
    "samsung electronics": "005930",
    "samsung": "005930",
    "sk hynix": "000660",
    "hynix": "000660",
    "hyundai motor": "005380",
    "naver": "035420",
    "kakao": "035720",
}


class MockSubAgentProvider(SubAgentProvider):
    def resolve_ticker(self, ticker: str | None, company_name: str | None) -> str | None:
        if ticker:
            return ticker

        if company_name is None:
            return None

        return COMPANY_NAME_TO_TICKER.get(company_name.strip().lower())

    def call(self, agent_name: str, ticker: str | None, query: str) -> SubAgentResponse:
        target_ticker = ticker or DEFAULT_TICKER
        execution_time_ms = random.randint(100, 800)

        handler = {
            "stock": self._stock,
            "news": self._news,
            "finance": self._finance,
            "disclosure": self._disclosure,
        }.get(agent_name)

        if handler is None:
            return SubAgentResponse.error(
                agent_name,
                f"Unsupported agent: {agent_name}",
                execution_time_ms,
            )

        return handler(target_ticker, execution_time_ms)

    def _stock(self, ticker: str, ms: int) -> SubAgentResponse:
        data = MOCK_STOCK_DATA.get(ticker)
        if data:
            return SubAgentResponse.success("stock", data, ms)
        return SubAgentResponse.no_data("stock", ms)

    def _news(self, ticker: str, ms: int) -> SubAgentResponse:
        signal_data = MOCK_NEWS_SIGNALS.get(ticker)
        if signal_data:
            signal = InvestmentSignalResponse(**signal_data)
            return SubAgentResponse.success_with_signal(signal, {"ticker": ticker}, ms)
        return SubAgentResponse.no_data("news", ms)

    def _finance(self, ticker: str, ms: int) -> SubAgentResponse:
        signal_data = MOCK_FINANCE_SIGNALS.get(ticker)
        if signal_data:
            signal = InvestmentSignalResponse(**signal_data)
            data = {
                "ticker": ticker,
                "stock_name": MOCK_STOCK_DATA.get(ticker, {}).get("stock_name"),
            }
            return SubAgentResponse.success_with_signal(signal, data, ms)
        return SubAgentResponse.no_data("finance", ms)

    def _disclosure(self, ticker: str, ms: int) -> SubAgentResponse:
        signal_data = MOCK_DISCLOSURE_SIGNALS.get(ticker)
        if signal_data:
            signal = InvestmentSignalResponse(**signal_data)
            return SubAgentResponse.success_with_signal(signal, {"ticker": ticker}, ms)
        return SubAgentResponse.no_data("disclosure", ms)
