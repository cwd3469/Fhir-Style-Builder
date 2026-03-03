from fastapi import APIRouter
from schemas import ChatRequest, ChatResponse
from services.claude_service import ClaudeService

router = APIRouter(prefix="/chat", tags=["chat"])

# 싱글턴 인스턴스 — 모듈 로드 시 한 번만 생성
_service = ClaudeService()

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    return _service.chat(request)