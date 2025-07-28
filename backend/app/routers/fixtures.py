from fastapi import APIRouter, Depends
from typing import Optional
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.fixture import Fixture

router = APIRouter()

@router.get("/fixtures")
def list_fixtures(gw_from: Optional[int] = None, gw_to: Optional[int] = None, session: Session = Depends(get_session)):
    stmt = select(Fixture)
    if gw_from is not None:
        stmt = stmt.where(Fixture.event >= gw_from)
    if gw_to is not None:
        stmt = stmt.where(Fixture.event <= gw_to)
    return session.exec(stmt).all()
