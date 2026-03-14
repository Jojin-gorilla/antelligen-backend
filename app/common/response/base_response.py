# 공통 응답 스키마 — 모든 API 응답은 이 포맷을 따른다.
# 팀원 가이드: success/fail 클래스메서드로 간단하게 반환 가능
#
# 사용 예시:
#   return BaseResponse.ok(data=my_dto)
#   return BaseResponse.fail("게시글을 찾을 수 없습니다.")

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool            # 요청 성공 여부
    message: str             # 사람이 읽을 수 있는 메시지
    data: Optional[T] = None # 실제 응답 데이터 (실패 시 None)

    @classmethod
    def ok(cls, data: T = None, message: str = "success") -> "BaseResponse[T]":
        """성공 응답 생성"""
        return cls(success=True, message=message, data=data)

    @classmethod
    def fail(cls, message: str) -> "BaseResponse[None]":
        """실패 응답 생성"""
        return cls(success=False, message=message, data=None)
