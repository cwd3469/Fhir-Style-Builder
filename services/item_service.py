from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Item
from schemas.item import ItemCreate, ItemUpdate

def get_all_items(db: Session):
    return db.query(Item).all()

def get_item(item_id: int, db: Session):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    return item


def create_item(item: ItemCreate, db: Session):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(item_id: int, item: ItemUpdate, db: Session):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")

    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(item_id: int, db: Session):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")

    db.delete(db_item)
    db.commit()
    return {"message": "삭제 완료", "id": item_id}