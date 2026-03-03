from fastapi import FastAPI
from database import engine
from models import Base
from routers import items, users , chat

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 라우터 등록
app.include_router(users.router)
app.include_router(items.router)
app.include_router(chat.router)  # 이제 router는 APIRouter 객체
