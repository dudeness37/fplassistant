from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.player import Player
from app.models.ep import EPRecord
from ortools.linear_solver import pywraplp

router = APIRouter()

def build_squad(session: Session, gw_start: int = 1, horizon: int = 6, budget: float = 100.0):
    ep_map: Dict[int, float] = {}
    for gw in range(gw_start, gw_start + horizon):
        for rec in session.exec(select(EPRecord).where(EPRecord.gw == gw)).all():
            ep_map[rec.fpl_element_id] = ep_map.get(rec.fpl_element_id, 0.0) + rec.ep

    players: List[Player] = session.exec(select(Player)).all()
    if not players or not ep_map:
        raise HTTPException(status_code=400, detail="No players/EP available. Ingest and compute EP first.")

    solver = pywraplp.Solver.CreateSolver("SCIP")
    x = {p.fpl_element_id: solver.BoolVar(f"x_{p.fpl_element_id}") for p in players}

    solver.Add(sum(x[p.fpl_element_id] for p in players) == 15)
    solver.Add(sum(x[p.fpl_element_id] for p in players if p.element_type == 1) == 2)
    solver.Add(sum(x[p.fpl_element_id] for p in players if p.element_type == 2) == 5)
    solver.Add(sum(x[p.fpl_element_id] for p in players if p.element_type == 3) == 5)
    solver.Add(sum(x[p.fpl_element_id] for p in players if p.element_type == 4) == 3)

    solver.Add(sum((p.now_cost/10.0) * x[p.fpl_element_id] for p in players) <= budget)

    teams: Dict[int, list[int]] = {}
    for p in players:
        teams.setdefault(p.team_id, []).append(p.fpl_element_id)
    for team_id, ids in teams.items():
        solver.Add(sum(x[i] for i in ids) <= 3)

    objective = solver.Objective()
    for p in players:
        objective.SetCoefficient(x[p.fpl_element_id], ep_map.get(p.fpl_element_id, 0.0))
    objective.SetMaximization()

    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        raise HTTPException(status_code=500, detail="Optimization failed")

    chosen = [p for p in players if x[p.fpl_element_id].solution_value() > 0.5]
    total_ep = sum(ep_map.get(p.fpl_element_id, 0.0) for p in chosen)
    total_cost = sum(p.now_cost/10.0 for p in chosen)
    return {
        "horizon": horizon,
        "gw_start": gw_start,
        "total_ep": round(total_ep, 2),
        "total_cost": round(total_cost, 1),
        "players": [
            {
                "id": p.fpl_element_id,
                "name": f"{p.first_name} {p.second_name}",
                "web_name": p.web_name,
                "pos": p.element_type,
                "team_id": p.team_id,
                "cost": p.now_cost/10.0,
                "ep_sum": round(ep_map.get(p.fpl_element_id, 0.0), 2)
            } for p in chosen
        ]
    }

@router.post("/optimize/squad")
def optimize_squad(gw_start: int = 1, horizon: int = 6, budget: float = 100.0, session: Session = Depends(get_session)):
    return build_squad(session, gw_start, horizon, budget)
