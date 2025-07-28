from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter()

@router.post("/telegram/register")
def register_user(payload: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.telegram_chat_id == payload.telegram_chat_id)).first()
    if existing:
        return {"msg": "already registered", "id": existing.id}
    user = User(telegram_chat_id=payload.telegram_chat_id)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"msg": "registered", "id": user.id}
