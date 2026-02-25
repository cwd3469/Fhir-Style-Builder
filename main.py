from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Item, Base

# 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

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


# ✅ CREATE - 아이템 생성
@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    global next_id
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    next_id += 1
    return db[next_id - 1]

# ✅ READ - 전체 조회
@app.get("/items/", response_model=list[ItemResponse])
def get_all_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

# ✅ READ - 단건 조회
@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    return item


# ✅ UPDATE - 수정
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = (
        db.query(Item)  # items 테이블 조회
        .filter(Item.id == item_id)  # Item 해당되는 id 컬럼값이 item_id 와 같은 행 필터링
        .first()  # 조건에 맞는 첫번째 행 가져오기
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")

    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


# ✅ DELETE - 삭제
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    db.delete(db_item)
    db.commit()
    return {"message": "삭제 완료", "id": item_id}