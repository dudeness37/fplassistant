from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.player import Player

router = APIRouter()

@router.get("/players", response_model=List[Player])
def list_players(pos: Optional[int] = None, team: Optional[int] = None, limit: int = 100, session: Session = Depends(get_session)):
    stmt = select(Player)
    if pos:
        stmt = stmt.where(Player.element_type == pos)
    if team:
        stmt = stmt.where(Player.team_id == team)
    stmt = stmt.limit(limit)
    return session.exec(stmt).all()
