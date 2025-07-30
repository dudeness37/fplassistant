import json, urllib.request, os
from sqlalchemy import create_engine, text

def get_json(url: str):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

print('Downloading fixtures…')
fx = get_json('https://fantasy.premierleague.com/api/fixtures/')

engine = create_engine(os.environ['DATABASE_URL'], pool_pre_ping=True, future=True)

with engine.begin() as conn:
    conn.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ux_fixtures_gw_ha ON fixtures(gw, home_team_id, away_team_id)'))

    # FPL team id -> internal teams.id
    team_map = {int(fpl): int(tid) for fpl,tid in conn.execute(text('SELECT fpl_team_id, team_id FROM teams_id_map'))}

    ins = text("""
      INSERT INTO fixtures (gw, home_team_id, away_team_id)
      VALUES (:gw, :home_id, :away_id)
      ON CONFLICT (gw, home_team_id, away_team_id) DO NOTHING
    """)

    inserted = 0
    for f in fx:
        gw = f.get('event')
        th = f.get('team_h')
        ta = f.get('team_a')
        if gw is None or th is None or ta is None:
            continue
        home_id = team_map.get(int(th))
        away_id = team_map.get(int(ta))
        if not home_id or not away_id:
            continue
        r = conn.execute(ins, {'gw': int(gw), 'home_id': int(home_id), 'away_id': int(away_id)})
        inserted += r.rowcount or 0

    total = conn.execute(text('SELECT COUNT(*) FROM fixtures')).scalar()
    print(f'Fixtures upsert ✓ inserted_now={inserted}, total={total}')
