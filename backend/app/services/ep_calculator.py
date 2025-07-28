from sqlmodel import Session, select
from math import exp
from app.models.player import Player
from app.models.fixture import Fixture
from app.models.team import Team
from app.models.ep import EPRecord

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + exp(-x))

def minutes_heuristic(p: Player) -> float:
    if p.element_type == 1:
        return 90.0
    if (p.status or 'a') != 'a':
        return 20.0
    m = p.minutes_prev or 0
    if m >= 2000:
        return 80.0
    if m >= 1000:
        return 65.0
    return 50.0

def goal_points(pos: int) -> int:
    return {1:6, 2:6, 3:5, 4:4}.get(pos, 4)

def clean_sheet_points(pos: int) -> int:
    return {1:4, 2:4, 3:1, 4:0}.get(pos, 0)

def ep_for_player_gw(session: Session, p: Player, gw: int) -> float:
    fix = session.exec(
        select(Fixture).where(Fixture.event == gw).where((Fixture.team_h == p.team_id) | (Fixture.team_a == p.team_id))
    ).first()
    if not fix:
        return 0.4
    opp_team_id = fix.team_a if fix.team_h == p.team_id else fix.team_h

    team = session.exec(select(Team).where(Team.fpl_team_id == p.team_id)).first()
    opp = session.exec(select(Team).where(Team.fpl_team_id == opp_team_id)).first()

    team_def = (team.strength_defence_home or team.strength or 100) + (team.strength_defence_away or 0)
    opp_att  = (opp.strength_attack_home or opp.strength or 100) + (opp.strength_attack_away or 0)

    cs_prob = sigmoid((team_def - opp_att) / 50.0)
    xmins = minutes_heuristic(p)
    appear_pts = 2.0 if xmins >= 60 else 1.0
    cs_pts = cs_prob * clean_sheet_points(p.element_type)

    mins_prev = max(1, p.minutes_prev or 1)
    g_per90 = (p.goals_prev or 0) / mins_prev * 90.0
    a_per90 = (p.assists_prev or 0) / mins_prev * 90.0
    att_pts_per90 = g_per90 * goal_points(p.element_type) + a_per90 * 3.0
    att_pts = att_pts_per90 * (xmins / 90.0)

    bonus = 0.2
    return float(appear_pts + cs_pts + att_pts + bonus)

def recompute_ep_range(session: Session, start_gw: int, end_gw: int) -> int:
    total = 0
    players = session.exec(select(Player)).all()
    for gw in range(start_gw, end_gw + 1):
        for existing in session.exec(select(EPRecord).where(EPRecord.gw == gw)).all():
            session.delete(existing)
        session.commit()

        for p in players:
            ep = ep_for_player_gw(session, p, gw)
            session.add(EPRecord(gw=gw, fpl_element_id=p.fpl_element_id, ep=ep))
            total += 1
        session.commit()
    return total
