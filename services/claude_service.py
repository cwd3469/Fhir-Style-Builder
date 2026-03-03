import os
from anthropic import Anthropic
from schemas import ChatRequest, ChatResponse

class ClaudeService:
    def __init__(self):
        # 인스턴스 생성 시 클라이언트 단 한 번 초기화 — 매 요청마다 생성 금지 (성능)
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
    def chat(self, request: ChatRequest) -> ChatResponse:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=request.max_tokens,
            messages=[m.model_dump() for m in request.messages]
        )
        return ChatResponse(
            content=response.content[0].text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens
        )