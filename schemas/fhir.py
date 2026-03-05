# schemas.py
from pydantic import BaseModel, field_validator
from typing import Optional, Literal
from fhir.resources.questionnaire import Questionnaire

# ── Input ──────────────────────────────────────────────────────
class FhirQuestionnaireRequest(BaseModel):
    """
    FHIR R5 Questionnaire를 받아서 React 컴포넌트 생성 요청
    """
    # FHIR R5 Questionnaire JSON - dict로 받아서 내부에서 R5 검증
    questionnaire: dict
    # 생성할 React 컴포넌트 이름 ex) "PatientIntakeForm"
    component_name: str
    # 스타일 라이브러리 선택 - 기본값 tailwind
    style_lib: Literal["tailwind", "emotion", "css-module"] = "tailwind"

    @field_validator("questionnaire")
    @classmethod
    def validate_fhir_questionnaire(cls, value: dict) -> dict:
        """
        FHIR R5 Questionnaire 유효성 검증
        - 실패 시 ValueError 발생 → FastAPI 422 응답
        """
        is_valid: bool = True
        error_message: str = ""
        try:
            Questionnaire.model_validate(value)
        except Exception as error:
            is_valid = False
            error_message = str(error)

        if not is_valid:
            raise ValueError(f"유효하지 않은 FHIR R5 Questionnaire: {error_message}")

        return value
    @field_validator("component_name")
    @classmethod
    def validate_component_name(cls, value: str) -> str:
        """
        React 컴포넌트 이름 규칙 검증
        - PascalCase 필수 ex) PatientForm
        """
        first_char: str = value[0]
        is_pascal_case: bool = first_char.isupper()
        if not is_pascal_case:
            raise ValueError("component_name은 PascalCase여야 합니다 ex) PatientForm")

        return value

# ── Output ─────────────────────────────────────────────────────
class FhirComponentResponse(BaseModel):
    """
    Claude가 생성한 React TSX 컴포넌트 응답
    """
    # TSX 코드 — 다운로드용
    component_code: str
    # 순수 HTML — iframe 렌더링용
    preview_html: str
    component_name: str
    fhir_item_count: int
    warnings: Optional[list[str]] = []


