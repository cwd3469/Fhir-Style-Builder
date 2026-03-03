from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from schemas import ItemCreate, ItemUpdate, ItemResponse
from services.item_service import get_all_items, get_item, create_item, update_item, delete_item
from routers.users import get_current_user
from models import User

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=list[ItemResponse])
def read_all_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_items(db)

@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_item(item_id, db)

@router.post("/", response_model=ItemResponse)
def write_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_item(item, db)

@router.put("/{item_id}", response_model=ItemResponse)
def modify_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_item(item_id, item, db)

@router.delete("/{item_id}")
def remove_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_item(item_id, db)
