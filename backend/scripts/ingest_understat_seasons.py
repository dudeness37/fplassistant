# backend/scripts/ingest_understat_seasons.py
import os, re, json, time
import requests
from sqlalchemy import create_engine, text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; fpl-ai/1.0; +https://github.com/dudeness37/fplassistant)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

SLEEP_BETWEEN = float(os.getenv("UNDERSTAT_SLEEP", "0.2"))
OFFSET = int(os.getenv("OFFSET", "0"))
LIMIT  = os.getenv("LIMIT")  # may be None

def safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default

def safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default

def get_provider_id(conn, code: str) -> int:
    return conn.execute(text("""
        SELECT id
        FROM external_providers
        WHERE UPPER(code)=UPPER(:c)
        LIMIT 1
    """), {"c": code}).scalar_one()

def fetch_understat_seasons(understat_id: str):
    """
    Returns a list (possibly empty) of season dicts.
    Never returns None.
    """
    url = f"https://understat.com/player/{understat_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 404:
            return []  # player page not found -> no data
        r.raise_for_status()
        html = r.text
    except Exception:
        return []  # network/HTTP error -> skip

    # Try to extract seasonsData = JSON.parse('....')
    # Handle escaped content & minor variations
    m = re.search(r"seasonsData\s*=\s*JSON\.parse\('([^']+)'\)", html)
    if not m:
        m = re.search(r"JSON\.parse\('([^']+)'\)\s*;?\s*\n", html)
    if not m:
        # Sometimes Understat changes markup; as a fallback, try a broader search
        m = re.search(r"seasonsData\s*=\s*JSON\.parse\((.*?)\)\s*;", html, re.DOTALL)
        if m:
            try:
                raw = m.group(1).strip()
                # raw is something like '"{...escaped json...}"'
                raw = json.loads(raw)  # unquote outer string
                return json.loads(raw) # parse JSON inside
            except Exception:
                return []
        return []

    try:
        raw = m.group(1).encode("utf-8").decode("unicode_escape")
        data = json.loads(raw)
        if isinstance(data, list):
            return data
        return []
    except Exception:
        return []

def main():
    engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)

    # Build the set of mapped players (with optional OFFSET/LIMIT)
    with engine.begin() as conn:
        prov_id = get_provider_id(conn, "UNDERSTAT")

        base_sql = """
            SELECT p.id AS player_id, pei.external_id AS understat_id
            FROM player_external_ids pei
            JOIN players p ON p.id = pei.player_id
            WHERE pei.provider_id = :prov
            ORDER BY p.id
        """
        if LIMIT:
            q = text(base_sql + " OFFSET :o LIMIT :l")
            rows = conn.execute(q, {"prov": prov_id, "o": OFFSET, "l": int(LIMIT)}).mappings().all()
        else:
            q = text(base_sql + " OFFSET :o")
            rows = conn.execute(q, {"prov": prov_id, "o": OFFSET}).mappings().all()

    total = len(rows)
    print(f"Ingesting Understat seasons for {total} players… (OFFSET={OFFSET}, LIMIT={LIMIT or 'ALL'})")
    upserts = 0

    with engine.begin() as conn:
        for i, r in enumerate(rows, 1):
            pid  = r["player_id"]
            usid = str(r["understat_id"])

            seasons = fetch_understat_seasons(usid)
            if not seasons:
                # No data for this player (new/unknown on Understat is normal)
                if i % 25 == 0:
                    print(f"  …{i}/{total} players processed (no seasons for some)")
                time.sleep(SLEEP_BETWEEN)
                continue

            for s in seasons:
                season   = str(s.get("season") or "")
                team     = (s.get("team_title") or s.get("team") or "").strip()
                comp     = (s.get("league") or "").strip()

                games    = safe_int(s.get("games"))
                starts   = safe_int(s.get("starts"))
                minutes  = safe_float(s.get("time"))
                goals    = safe_float(s.get("goals"))
                assists  = safe_float(s.get("assists"))
                shots    = safe_float(s.get("shots"))
                key_ps   = safe_float(s.get("key_passes"))
                xg       = safe_float(s.get("xG"))
                xa       = safe_float(s.get("xA"))
                nineties = (minutes / 90.0) if minutes else 0.0

                # Normalize for unique index
                team = team or ""
                comp = comp or ""

                conn.execute(text("""
                  INSERT INTO external_player_seasons
                    (player_id, provider_id, season, team, comp,
                     minutes, goals, assists, xg, xa, shots, key_passes, nineties, updated_at)
                  VALUES
                    (:player_id, :prov, :season, :team, :comp,
                     :minutes, :goals, :assists, :xg, :xa, :shots, :kp, :n90, NOW())
                  ON CONFLICT (player_id, provider_id, season, team, comp)
                  DO UPDATE SET
                    minutes    = EXCLUDED.minutes,
                    goals      = EXCLUDED.goals,
                    assists    = EXCLUDED.assists,
                    xg         = EXCLUDED.xg,
                    xa         = EXCLUDED.xa,
                    shots      = EXCLUDED.shots,
                    key_passes = EXCLUDED.key_passes,
                    nineties   = EXCLUDED.nineties,
                    updated_at = NOW()
                """), {
                    "player_id": pid, "prov": prov_id, "season": season,
                    "team": team, "comp": comp,
                    "minutes": minutes, "goals": goals, "assists": assists,
                    "xg": xg, "xa": xa, "shots": shots, "kp": key_ps, "n90": nineties
                })
                upserts += 1

            if i % 25 == 0:
                print(f"  …{i}/{total} players processed")
            time.sleep(SLEEP_BETWEEN)

    print(f"Understat seasons ingest ✓ rows upserted≈{upserts}")

if __name__ == "__main__":
    main()
