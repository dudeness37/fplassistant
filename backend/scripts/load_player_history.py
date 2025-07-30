import json, urllib.request, os, time
from sqlalchemy import create_engine, text

SEASON = os.environ.get('SEASON', '2024/25')
LIMIT  = int(os.environ.get('LIMIT', '0'))  # 0 = all

def get_json(url: str):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

engine = create_engine(os.environ['DATABASE_URL'], pool_pre_ping=True, future=True)

with engine.begin() as conn:
    conn.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ux_player_gw_stats_player_gw_season ON player_gw_stats(player_id, gw, season)'))

players = []
with engine.connect() as conn:
    q = text('SELECT p.id, pim.fpl_id FROM players p JOIN players_id_map pim ON pim.player_id = p.id ORDER BY p.id')
    for row in conn.execute(q):
        players.append((int(row.id), int(row.fpl_id)))

if LIMIT and LIMIT > 0:
    players = players[:LIMIT]

print(f'Fetching element summaries for {len(players)} players… (season={SEASON})')

ins = text("""
  INSERT INTO player_gw_stats
    (player_id, gw, season, minutes, points, xG, xA, shots, key_passes, bonus)
  VALUES
    (:player_id, :gw, :season, :minutes, :points, :xg, :xa, :shots, :kp, :bonus)
  ON CONFLICT (player_id, gw, season) DO UPDATE
    SET minutes = EXCLUDED.minutes,
        points  = EXCLUDED.points,
        xG      = EXCLUDED.xG,
        xA      = EXCLUDED.xA,
        shots   = EXCLUDED.shots,
        key_passes = EXCLUDED.key_passes,
        bonus   = EXCLUDED.bonus
""")

inserted = 0
with engine.begin() as conn:
    for i, (pid, fid) in enumerate(players, 1):
        try:
            data = get_json(f'https://fantasy.premierleague.com/api/element-summary/{fid}/')
        except Exception as e:
            print(f'  ! skip fpl_id={fid}: {e}')
            continue

        # Current season GW logs
        for h in data.get('history', []):
            gw = int(h.get('round') or 0)
            if not gw:
                continue
            payload = {
                'player_id': pid,
                'gw': gw,
                'season': SEASON,
                'minutes': int(h.get('minutes') or 0),
                'points':  int(h.get('total_points') or 0),
                'xg': float(h.get('expected_goals') or 0.0),
                'xa': float(h.get('expected_assists') or 0.0),
                # FPL element history doesn’t include shots/key_passes — store 0 (OK for now)
                'shots': int(h.get('shots') or 0),
                'kp': int(h.get('key_passes') or 0),
                'bonus': int(h.get('bonus') or 0),
            }
            r = conn.execute(ins, payload)
            inserted += r.rowcount or 0

        if i % 25 == 0:
            print(f'  …{i}/{len(players)} players done')
        time.sleep(0.3)  # be kind to FPL

print(f'Player GW history upsert ✓ inserted_rows≈{inserted}')
