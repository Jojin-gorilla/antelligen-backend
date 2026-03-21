from fastapi import APIRouter

from app.common.response.base_response import BaseResponse
from app.domains.agent.adapter.outbound.external.mock_sub_agent_provider import (
    MockSubAgentProvider,
)
from app.domains.agent.application.request.agent_query_request import AgentQueryRequest
from app.domains.agent.application.request.finance_analysis_request import (
    FinanceAnalysisRequest,
)
from app.domains.agent.application.response.frontend_agent_response import (
    FrontendAgentResponse,
)
from app.domains.agent.application.usecase.process_agent_query_usecase import (
    ProcessAgentQueryUseCase,
)

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post(
    "/query",
    response_model=BaseResponse[FrontendAgentResponse],
    status_code=200,
)
async def query_agent(request: AgentQueryRequest):
    provider = MockSubAgentProvider()
    usecase = ProcessAgentQueryUseCase(provider)
    internal_result = usecase.execute(request)
    frontend_result = FrontendAgentResponse.from_internal(internal_result)
    return BaseResponse.ok(data=frontend_result)


@router.post(
    "/finance-analysis",
    response_model=BaseResponse[FrontendAgentResponse],
    status_code=200,
)
async def analyze_finance(request: FinanceAnalysisRequest):
    provider = MockSubAgentProvider()
    usecase = ProcessAgentQueryUseCase(provider)
    resolved_ticker = provider.resolve_ticker(request.ticker, request.company_name)

    internal_result = usecase.execute(
        AgentQueryRequest(
            query=request.query,
            ticker=resolved_ticker,
            session_id=request.session_id,
            user_profile=request.user_profile,
            options={"agents": ["finance"], "max_tokens": 1024},
        )
    )
    frontend_result = FrontendAgentResponse.from_internal(internal_result)
    return BaseResponse.ok(data=frontend_result)
