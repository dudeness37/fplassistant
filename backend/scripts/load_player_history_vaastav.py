# /app/scripts/load_player_history_vaastav.py
import os, csv, io, sys, time
from typing import Optional
import requests
from sqlalchemy import create_engine, text

# Env
DATABASE_URL = os.environ["DATABASE_URL"]  # already points to Neon (postgresql+psycopg://...)
SEASON = os.environ.get("SEASON", "2023/24")   # season label stored in DB
FROM_GW = int(os.environ.get("FROM_GW", "1"))
TO_GW   = int(os.environ.get("TO_GW", "38"))

# Map '2023/24' -> '2023-24' folder name in vaastav repo
def season_folder(season_text: str) -> str:
    # 'YYYY/YY' -> 'YYYY-YY'
    return season_text.replace("/", "-")

def gw_csv_url(season_text: str, gw: int) -> str:
    base = "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data"
    return f"{base}/{season_folder(season_text)}/gws/gw{gw}.csv"

def get_csv(url: str) -> Optional[str]:
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200 and r.text.strip():
            return r.text
        return None
    except Exception as e:
        print(f"  WARN: fetch failed {url}: {e}")
        return None

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Prepare statements
UPSERT_SQL = text("""
INSERT INTO player_gw_stats
  (player_id, season, gw, minutes, points, xG, xA, shots, key_passes, bonus)
VALUES
  (:player_id, :season, :gw, :minutes, :points, :xg, :xa, :shots, :key_passes, :bonus)
ON CONFLICT ON CONSTRAINT ux_player_gw_stats_player_gw_season
DO UPDATE SET
  minutes      = EXCLUDED.minutes,
  points       = EXCLUDED.points,
  xG           = EXCLUDED.xG,
  xA           = EXCLUDED.xA,
  shots        = EXCLUDED.shots,
  key_passes   = EXCLUDED.key_passes,
  bonus        = EXCLUDED.bonus;
""")

# Build a dict fpl_id -> player_id (internal)
with engine.connect() as conn:
    rows = conn.execute(text("SELECT fpl_id, player_id FROM players_id_map")).fetchall()
fpl_to_internal = {int(r[0]): int(r[1]) for r in rows if r[0] is not None and r[1] is not None}
print(f"Loaded players_id_map: {len(fpl_to_internal)} mappings")

inserted = 0
skipped_no_map = 0
skipped_rows = 0

for gw in range(FROM_GW, TO_GW + 1):
    url = gw_csv_url(SEASON, gw)
    print(f"Fetching GW{gw} CSV… {url}")
    csv_text = get_csv(url)
    if not csv_text:
        print(f"  GW{gw}: no CSV found (maybe season/gw missing in repo).")
        continue

    buf = io.StringIO(csv_text)
    reader = csv.DictReader(buf)
    batch = []
    for row in reader:
        # vaastav columns vary by season but commonly include:
        # element (FPL player id), minutes, total_points, xG, xA, shots, key_passes, bonus
        try:
            fpl_id = int(row.get("element") or 0)
        except:
            fpl_id = 0
        if not fpl_id:
            skipped_rows += 1
            continue

        player_id = fpl_to_internal.get(fpl_id)
        if not player_id:
            skipped_no_map += 1
            continue

        def to_int(x, default=0):
            try:
                return int(float(x))
            except:
                return default

        def to_float(x, default=None):
            try:
                return float(x)
            except:
                return default

        minutes = to_int(row.get("minutes"))
        points  = to_float(row.get("total_points"), 0.0)
        xg      = to_float(row.get("xG"))
        xa      = to_float(row.get("xA"))
        shots   = to_int(row.get("shots"))
        kps     = to_int(row.get("key_passes"))
        bonus   = to_int(row.get("bonus"))

        batch.append({
            "player_id": player_id,
            "season": SEASON,
            "gw": gw,
            "minutes": minutes,
            "points": points,
            "xg": xg,
            "xa": xa,
            "shots": shots,
            "key_passes": kps,
            "bonus": bonus
        })

    if not batch:
        print(f"  GW{gw}: nothing to insert")
        continue

    with engine.begin() as conn:
        for rec in batch:
            conn.execute(UPSERT_SQL, rec)
            inserted += 1

    print(f"  GW{gw}: upserted {len(batch)} rows")

print(f"Done. Inserted/updated rows: {inserted}, skipped_no_map={skipped_no_map}, skipped_rows={skipped_rows}")
