import json, urllib.request, os
from sqlalchemy import create_engine, text

def get_json(url: str):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

print('Downloading bootstrap-static…')
bs = get_json('https://fantasy.premierleague.com/api/bootstrap-static/')

teams_api = bs['teams']
elements  = bs['elements']
pos_map   = {1:'GK', 2:'DEF', 3:'MID', 4:'FWD'}

engine = create_engine(os.environ['DATABASE_URL'], pool_pre_ping=True, future=True)

with engine.begin() as conn:
    # Safety: indexes / helper maps
    conn.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ux_teams_short ON teams(short_name)'))
    conn.execute(text('CREATE TABLE IF NOT EXISTS teams_id_map (team_id INT REFERENCES teams(id) ON DELETE CASCADE, fpl_team_id INT UNIQUE NOT NULL)'))
    conn.execute(text('CREATE TABLE IF NOT EXISTS players_id_map (player_id INT REFERENCES players(id) ON DELETE CASCADE, fpl_id INT UNIQUE NOT NULL)'))

    # --- Upsert teams; build {fpl_team_id -> teams.id}
    team_map = {}
    for t in teams_api:
        params = {'name': t['name'], 'short': t['short_name']}
        team_id = conn.execute(text("""
            INSERT INTO teams (name, short_name)
            VALUES (:name, :short)
            ON CONFLICT (short_name) DO UPDATE
              SET name = EXCLUDED.name
            RETURNING id
        """), params).scalar_one()
        team_map[int(t['id'])] = int(team_id)
        conn.execute(text("""
            INSERT INTO teams_id_map (team_id, fpl_team_id)
            VALUES (:team_id, :fpl)
            ON CONFLICT (fpl_team_id) DO UPDATE
              SET team_id = EXCLUDED.team_id
        """), {'team_id': team_id, 'fpl': int(t['id'])})

    # --- Upsert players; build display name; update id map
    rows = []
    for e in elements:
        first  = (e.get('first_name') or '').strip()
        second = (e.get('second_name') or '').strip()
        web    = (e.get('web_name') or '').strip()
        name   = (f'{first} {second}'.strip()) or web
        rows.append({
            'fpl_id': int(e['id']),
            'name': name,
            'position': pos_map.get(int(e['element_type']), None),
            'team_id': team_map.get(int(e['team'])),
            'price': float(e.get('now_cost', 0) or 0) / 10.0,
            'own': float((e.get('selected_by_percent') or '0').replace('%','') or 0.0),
            'status': (e.get('status') or '').strip()
        })

    ins = text("""
      INSERT INTO players (fpl_id, name, position, team_id, price, ownership_percent, status)
      VALUES (:fpl_id, :name, :position, :team_id, :price, :own, :status)
      ON CONFLICT (fpl_id) DO UPDATE
        SET name = EXCLUDED.name,
            position = EXCLUDED.position,
            team_id = EXCLUDED.team_id,
            price = EXCLUDED.price,
            ownership_percent = EXCLUDED.ownership_percent,
            status = EXCLUDED.status
      RETURNING id, fpl_id
    """)

    upserts = 0
    for r in rows:
        pid, fid = conn.execute(ins, r).one()
        upserts += 1
        conn.execute(text("""
          INSERT INTO players_id_map (player_id, fpl_id)
          VALUES (:player_id, :fpl_id)
          ON CONFLICT (fpl_id) DO UPDATE
            SET player_id = EXCLUDED.player_id
        """), {'player_id': pid, 'fpl_id': fid})

    teams_cnt   = conn.execute(text("SELECT COUNT(*) FROM teams")).scalar()
    players_cnt = conn.execute(text("SELECT COUNT(*) FROM players")).scalar()
    print(f'Loaded teams & players ✓  teams={teams_cnt}, players={players_cnt}, player_upserts={upserts}')
