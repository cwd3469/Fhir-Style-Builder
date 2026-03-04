from fastapi import APIRouter, HTTPException
from schemas.fhir import FhirQuestionnaireRequest, FhirComponentResponse
from services.fhir_claude_service import FhirClaudeService

# 라우터 인스턴스 생성
router: APIRouter = APIRouter(
    prefix="/fhir",
    tags=["fhir"]
)

fhir_claude_service: FhirClaudeService = FhirClaudeService()

@router.post("/generate", response_model=FhirComponentResponse)
def generate_fhir_component(request: FhirQuestionnaireRequest) -> FhirComponentResponse:
    """
    FHIR R5 Questionnaire → React TSX 컴포넌트 생성
    """
    is_success: bool = True
    error_message: str = ""
    result: FhirComponentResponse = None
    try:
        result = fhir_claude_service.generate_component(request)
    except Exception as error:
        is_success = False
        error_message = str(error)

    if not is_success:
        raise HTTPException(status_code=500, detail=error_message)

    return result

