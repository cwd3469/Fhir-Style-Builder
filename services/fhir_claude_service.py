import os
import json
from anthropic import Anthropic
from fhir.resources.questionnaire import Questionnaire
from schemas.fhir import FhirQuestionnaireRequest, FhirComponentResponse

class FhirClaudeService:
    def __init__(self):
        # 인스턴스 생성 시 클라이언트 단 한 번 초기화 — 매 요청마다 생성 금지 (성능)
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
    def generate_component(self, request: FhirQuestionnaireRequest) -> FhirComponentResponse:
        """
        FHIR R5 Questionnaire → React TSX 컴포넌트 생성
        1. FHIR item 목록 추출
        2. Claude에게 TSX 생성 요청
        3. FhirComponentResponse 반환
        """
        # 1. FHIR Questionnaire 파싱 — item 목록 추출
        questionnaire_model: Questionnaire = Questionnaire.model_validate(
            request.questionnaire
        )
        fhir_items: list = questionnaire_model.item if questionnaire_model.item else []
        fhir_item_count: int = len(fhir_items)
        # 2. 프롬프트 구성
        prompt: str = self._build_prompt(
            questionnaire=request.questionnaire,
            component_name=request.component_name,
            style_lib=request.style_lib,
            fhir_item_count=fhir_item_count
        )
        # 3. Claude API 호출
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        # 4. 응답 텍스트 추출
        raw_text: str = response.content[0].text

        # 5. JSON 파싱
        parsed: dict = json.loads(raw_text)

        # 6. FhirComponentResponse 반환
        return FhirComponentResponse(
            component_code=parsed["component_code"],
            component_name=request.component_name,
            fhir_item_count=fhir_item_count,
            warnings=parsed.get("warnings", [])
        )

    def _build_prompt(
            self,
            questionnaire: dict,
            component_name: str,
            style_lib: str,
            fhir_item_count: int
    ) -> str:
        """
        Claude에게 전달할 프롬프트 구성
        - JSON만 반환하도록 강제
        - TSX 코드 + warnings 구조
        """
        questionnaire_json: str = json.dumps(questionnaire, ensure_ascii=False, indent=2)
        prompt: str = f"""
        다음 FHIR R5 Questionnaire JSON을 분석하여 React TypeScript 컴포넌트를 생성하라.
        총 {fhir_item_count}개의 item이 있다.

        FHIR Questionnaire:
        {questionnaire_json}

        요구사항:
        - 컴포넌트 이름: {component_name}
        - 스타일 라이브러리: {style_lib}
        - TypeScript 타입 명시 필수
        - 각 FHIR item의 type에 맞는 input 요소 사용
          - string → <input type="text" />
          - boolean → <input type="checkbox" />
          - integer → <input type="number" />
          - choice → <select />
          - date → <input type="date" />
        - FHIR item의 required 필드 반영
        - linkId를 각 input의 name 속성으로 사용

        반드시 아래 JSON 형식으로만 응답하라. 마크다운 코드블록 없이 JSON만 반환하라:
        {{
            "component_code": "생성된 TSX 코드 전체",
            "warnings": ["처리하지 못한 item이 있으면 경고 메시지", "없으면 빈 배열"]
        }}
        """
        return prompt
