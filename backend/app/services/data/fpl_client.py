from sqlmodel import Session, select
import httpx
from app.models.team import Team
from app.models.player import Player
from app.models.fixture import Fixture

BOOTSTRAP = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES = "https://fantasy.premierleague.com/api/fixtures/"

def ingest_bootstrap(session: Session):
    r = httpx.get(BOOTSTRAP, timeout=30.0)
    r.raise_for_status()
    data = r.json()

    teams = data.get("teams", [])
    for t in teams:
        obj = session.exec(select(Team).where(Team.fpl_team_id == t["id"])).first()
        if not obj:
            obj = Team(
                fpl_team_id=t["id"],
                name=t["name"],
                short_name=t["short_name"],
                strength=t.get("strength"),
                strength_attack_home=t.get("strength_attack_home"),
                strength_attack_away=t.get("strength_attack_away"),
                strength_defence_home=t.get("strength_defence_home"),
                strength_defence_away=t.get("strength_defence_away"),
            )
            session.add(obj)
        else:
            obj.name = t["name"]
            obj.short_name = t["short_name"]
            obj.strength = t.get("strength")
            obj.strength_attack_home = t.get("strength_attack_home")
            obj.strength_attack_away = t.get("strength_attack_away")
            obj.strength_defence_home = t.get("strength_defence_home")
            obj.strength_defence_away = t.get("strength_defence_away")

    players = data.get("elements", [])
    for p in players:
        obj = session.exec(select(Player).where(Player.fpl_element_id == p["id"])).first()
        fields = dict(
            fpl_element_id=p["id"],
            first_name=p.get("first_name",""),
            second_name=p.get("second_name",""),
            web_name=p.get("web_name",""),
            team_id=p.get("team"),
            element_type=p.get("element_type"),
            now_cost=p.get("now_cost",0),
            status=p.get("status","a"),
            minutes_prev=p.get("minutes",0),
            goals_prev=p.get("goals_scored",0),
            assists_prev=p.get("assists",0),
        )
        if not obj:
            session.add(Player(**fields))
        else:
            for k,v in fields.items():
                setattr(obj, k, v)

    session.commit()
    return {"teams": len(teams), "players": len(players)}

def ingest_fixtures(session: Session):
    r = httpx.get(FIXTURES, timeout=30.0)
    r.raise_for_status()
    fixtures = r.json()
    count = 0
    for f in fixtures:
        obj = session.exec(select(Fixture).where(Fixture.fpl_fixture_id == f["id"])).first()
        if not obj:
            obj = Fixture(
                fpl_fixture_id=f["id"],
                event=f.get("event"),
                team_h=f["team_h"],
                team_a=f["team_a"],
                finished=f.get("finished", False),
            )
            session.add(obj)
            count += 1
        else:
            obj.event = f.get("event")
            obj.team_h = f["team_h"]
            obj.team_a = f["team_a"]
            obj.finished = f.get("finished", False)
    session.commit()
    return count
