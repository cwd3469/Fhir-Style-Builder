# FHIR Form Builder AI — Backend

> FHIR R5 Questionnaire JSON → React TypeScript 컴포넌트 자동 생성 API

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![Claude API](https://img.shields.io/badge/Claude-claude--sonnet--4-D97757?style=flat-square&logo=anthropic&logoColor=white)
![FHIR](https://img.shields.io/badge/FHIR-R5-E84343?style=flat-square)

---

## 데모

> GIF 데모 이미지 삽입 위치
> `![demo](./docs/demo.gif)`

---

## 프로젝트 개요

의료 현장에서 FHIR Questionnaire 기반 문진 폼을 개발할 때, 매번 반복적인 React 컴포넌트 작성이 필요하다.  
이 프로젝트는 **FHIR R5 Questionnaire JSON을 입력하면 Claude AI가 즉시 React TSX 컴포넌트를 생성**하는 API 서버다.

### 핵심 플로우

```
FHIR R5 Questionnaire JSON
        ↓
FastAPI (R5 유효성 검증)
        ↓
Claude claude-sonnet-4 API
        ↓
React TypeScript 컴포넌트 코드
```

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| Framework | FastAPI |
| AI | Anthropic Claude claude-sonnet-4 |
| FHIR 검증 | fhir.resources 8.2.0 (R5) |
| 데이터 검증 | Pydantic v2 |
| 인증 | JWT |
| DB | SQLAlchemy |

---

## 프로젝트 구조

```
backend/
├── main.py                     # FastAPI 앱 진입점, CORS 설정
├── routers/
│   └── fhir.py                 # /fhir/generate 엔드포인트
├── services/
│   └── fhir_claude_service.py  # Claude API 호출 + TSX 생성 핵심 로직
├── schemas/
│   └── fhir.py                 # FHIR R5 요청/응답 Pydantic 스키마
├── models.py                   # DB 모델
└── database.py                 # DB 연결
```

---

## 핵심 기능

### FHIR R5 유효성 검증
```python
# fhir.resources 8.2.0 R5 패키지로 입력 데이터 검증
from fhir.resources.questionnaire import Questionnaire

Questionnaire.model_validate(request.questionnaire)
# 유효하지 않은 FHIR R5 → 422 Unprocessable Entity 자동 반환
```

### Claude API FHIR item 타입 매핑
| FHIR item type | 생성되는 React 컴포넌트 |
|----------------|------------------------|
| `string` | `<input type="text" />` |
| `boolean` | `<input type="checkbox" />` |
| `integer` | `<input type="number" />` |
| `choice` | `<select />` |
| `date` | `<input type="date" />` |

---

## 시작하기

### 요구사항
- Python 3.11+
- Anthropic API Key

### 설치

```bash
# 레포 클론
git clone https://github.com/cwd3469/Fhir-Style-Builder.git
cd Fhir-Style-Builder

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 환경변수 설정

```bash
# .env 파일 생성
cp .env.example .env
```

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your_secret_key
```

### 서버 실행

```bash
uvicorn main:app --reload
```

API 문서: `http://localhost:8000/docs`

---

## API 명세

### `POST /fhir/generate`

FHIR R5 Questionnaire → React TSX 컴포넌트 생성

**Request**
```json
{
  "questionnaire": {
    "resourceType": "Questionnaire",
    "status": "active",
    "item": [
      {"linkId": "1", "text": "환자 이름", "type": "string", "required": true},
      {"linkId": "2", "text": "생년월일", "type": "date", "required": true},
      {"linkId": "3", "text": "흡연 여부", "type": "boolean", "required": false}
    ]
  },
  "component_name": "PatientForm",
  "style_lib": "tailwind"
}
```

**Response**
```json
{
  "component_code": "import React, { useState } from 'react';\n...",
  "component_name": "PatientForm",
  "fhir_item_count": 3,
  "warnings": []
}
```

**Error**
| Status | 설명 |
|--------|------|
| `400` | 존재하지 않은 |
| `422` | 유효하지 않은 FHIR R5 Questionnaire |
| `500` | Claude API 호출 실패 |

---

## 관련 레포

- **Frontend**: [Fhir-Style-Builder-Front](https://github.com/cwd3469/Fhir-Style-Builder-Front)
