import asyncio
import logging
from datetime import date, timedelta
from typing import List

from app.domains.dashboard.application.port.out.fred_macro_port import FredMacroPort
from app.domains.dashboard.application.response.economic_event_response import (
    EconomicEventResponse,
    EconomicEventsResponse,
)
from app.domains.dashboard.domain.entity.economic_event import EconomicEvent
from app.domains.dashboard.domain.entity.macro_data_point import MacroDataPoint

logger = logging.getLogger(__name__)

# period → 날짜 범위(일) 매핑
_PERIOD_TO_DAYS: dict[str, int] = {
    "1D": 365,
    "1W": 1_095,
    "1M": 1_825,
    "1Y": 7_300,
}

# FRED Series ID → (이벤트 타입, 라벨)
_SERIES_CONFIG: dict[str, tuple[str, str]] = {
    "FEDFUNDS": ("INTEREST_RATE", "기준금리"),
    "CPIAUCSL": ("CPI", "CPI"),
    "UNRATE":   ("UNEMPLOYMENT", "실업률"),
}


def _to_events(
    full_data: List[MacroDataPoint],
    event_type: str,
    label: str,
    start_date: date,
) -> List[EconomicEvent]:
    """전체 시리즈에서 start_date 이후 데이터만 이벤트로 변환한다.

    previous는 full_data 기준 직전 인덱스 값을 사용해
    필터링 경계에서도 정확한 이전 발표값을 반환한다.
    """
    events: List[EconomicEvent] = []
    for i, point in enumerate(full_data):
        if point.date < start_date:
            continue
        previous = full_data[i - 1].value if i > 0 else None
        events.append(
            EconomicEvent(
                event_id=f"{event_type}-{point.date.strftime('%Y-%m-%d')}",
                type=event_type,
                label=label,
                date=point.date,
                value=point.value,
                previous=previous,
                forecast=None,
            )
        )
    return events


def _yoy(current: float, year_ago: float) -> float:
    return round((current - year_ago) / year_ago * 100, 2)


def _to_cpi_yoy_events(
    full_data: List[MacroDataPoint],
    event_type: str,
    label: str,
    start_date: date,
) -> List[EconomicEvent]:
    """CPI 데이터를 전년 동월 대비 변화율(%)로 변환한다.

    계산식: (현재 지수 - 1년 전 지수) / 1년 전 지수 × 100
    전년 동월 값이 없는 포인트는 건너뛴다.
    """
    date_to_value = {p.date: p.value for p in full_data}

    events: List[EconomicEvent] = []
    for i, point in enumerate(full_data):
        if point.date < start_date:
            continue

        year_ago_date = point.date.replace(year=point.date.year - 1)
        year_ago_value = date_to_value.get(year_ago_date)
        if not year_ago_value:
            continue

        previous_yoy: float | None = None
        if i > 0:
            prev = full_data[i - 1]
            prev_year_ago_date = prev.date.replace(year=prev.date.year - 1)
            prev_year_ago_value = date_to_value.get(prev_year_ago_date)
            if prev_year_ago_value:
                previous_yoy = _yoy(prev.value, prev_year_ago_value)

        events.append(
            EconomicEvent(
                event_id=f"{event_type}-{point.date.strftime('%Y-%m-%d')}",
                type=event_type,
                label=label,
                date=point.date,
                value=_yoy(point.value, year_ago_value),
                previous=previous_yoy,
                forecast=None,
            )
        )
    return events


class GetEconomicEventsUseCase:

    def __init__(self, fred_macro_port: FredMacroPort):
        self._fred = fred_macro_port

    async def execute(self, period: str) -> EconomicEventsResponse:
        """period 기준 날짜 범위 내 경제 이벤트 목록을 반환한다.

        Args:
            period: "1D" | "1W" | "1M" | "1Y"
                1D → 365일 / 1W → 1,095일 / 1M → 1,825일 / 1Y → 7,300일

        Returns:
            EconomicEventsResponse
        """
        days = _PERIOD_TO_DAYS[period]
        start_date = date.today() - timedelta(days=days)

        # previous 값 확보를 위해 period보다 2개월 더 넉넉하게 fetch
        fetch_months = days // 30 + 2
        # CPI YoY 계산을 위해 12개월 추가 fetch (전년 동월 값 확보)
        cpi_fetch_months = fetch_months + 12

        fedfunds_data, cpiaucsl_data, unrate_data = await asyncio.gather(
            self._fred.fetch_series("FEDFUNDS", fetch_months),
            self._fred.fetch_series("CPIAUCSL", cpi_fetch_months),
            self._fred.fetch_series("UNRATE", fetch_months),
        )

        all_events: List[EconomicEvent] = []
        for series_id, data in [
            ("FEDFUNDS", fedfunds_data),
            ("CPIAUCSL", cpiaucsl_data),
            ("UNRATE", unrate_data),
        ]:
            event_type, label = _SERIES_CONFIG[series_id]
            if series_id == "CPIAUCSL":
                all_events.extend(_to_cpi_yoy_events(data, event_type, label, start_date))
            else:
                all_events.extend(_to_events(data, event_type, label, start_date))

        # 날짜 오름차순 정렬
        all_events.sort(key=lambda e: e.date)

        logger.info(
            "[GetEconomicEvents] 완료: period=%s, total_events=%d",
            period,
            len(all_events),
        )

        return EconomicEventsResponse(
            period=period,
            count=len(all_events),
            events=[EconomicEventResponse.from_entity(e) for e in all_events],
        )
