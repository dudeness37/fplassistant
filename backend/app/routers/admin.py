from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.services.data.fpl_client import ingest_bootstrap, ingest_fixtures
from app.services.ep_calculator import recompute_ep_range

router = APIRouter()

@router.post("/ingest/fpl")
def ingest_fpl(session: Session = Depends(get_session)):
    stats = ingest_bootstrap(session)
    return {"msg": "ok", "players": stats.get("players", 0), "teams": stats.get("teams", 0)}

@router.post("/ingest/fixtures")
def ingest_fix(session: Session = Depends(get_session)):
    n = ingest_fixtures(session)
    return {"msg": "ok", "fixtures": n}

@router.post("/ingest/all")
def ingest_all(session: Session = Depends(get_session)):
    s1 = ingest_bootstrap(session)
    n = ingest_fixtures(session)
    return {"msg": "ok", "players": s1.get("players",0), "teams": s1.get("teams",0), "fixtures": n}

@router.post("/ep/recompute")
def ep_recompute(start_gw: int = 1, end_gw: int = 6, session: Session = Depends(get_session)):
    total = recompute_ep_range(session, start_gw, end_gw)
    return {"msg": "ok", "records": total}
