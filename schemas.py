from pydantic import BaseModel
from typing import Optional , Literal

# 유저 관련
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# 토큰 관련
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# Pydantic 스키마
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        orm_mode = True  # SQLAlchemy 객체 → Pydantic 변환


# TypeScript의 interface Message { role: "user" | "assistant"; content: string }
class Message(BaseModel):
    role: Literal["user", "assistant"]  # union type 그대로
    content: str

# Request DTO
class ChatRequest(BaseModel):
    messages: list[Message]
    max_tokens: int = 1024  # 기본값 설정

# Response DTO
class ChatResponse(BaseModel):
    content: str
    input_tokens: int
    output_tokens: int