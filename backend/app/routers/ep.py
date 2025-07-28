from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.ep import EPRecord
from app.models.player import Player

router = APIRouter()

@router.get("/ep/top")
def ep_top(gw: int, pos: int | None = None, limit: int = 20, session: Session = Depends(get_session)):
    stmt = select(EPRecord, Player).where(EPRecord.gw == gw).join(Player, Player.fpl_element_id == EPRecord.fpl_element_id)
    if pos:
        stmt = stmt.where(Player.element_type == pos)
    rows = session.exec(stmt).all()
    rows.sort(key=lambda r: r[0].ep, reverse=True)
    rows = rows[:limit]
    return [
        {
            "player_id": p.fpl_element_id,
            "name": f"{p.first_name} {p.second_name}",
            "web_name": p.web_name,
            "team_id": p.team_id,
            "pos": p.element_type,
            "cost": p.now_cost / 10.0,
            "ep": round(ep.ep, 2)
        }
        for ep, p in rows
    ]
