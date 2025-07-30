# /app/scripts/map_fbref_ids.py
import os, time, re
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; fpl-ai-mapper/1.0; +https://github.com/dudeness37/fplassistant)"
}

FBREF_COMPS = os.environ.get(
    "FBREF_COMPS",
    # comp codes: EPL=9, Championship=10, La Liga=12, Serie A=11, Bundesliga=20, Ligue1=13, UCL=8, UEL=19
    "9,10,12,11,20,13,8,19"
).split(",")

SEASONS = os.environ.get("FBREF_SEASONS", "2024-2025,2023-2024,2022-2023").split(",")

BATCH = int(os.environ.get("BATCH", "300"))
OFFSET = int(os.environ.get("OFFSET", "0"))
SLEEP = float(os.environ.get("SLEEP", "0.8"))

def norm(s: str) -> str:
    return re.sub(r'\s+', ' ', (s or "").strip().lower())

def fetch_comp_players(comp_code: str, season: str):
    # Example: https://fbref.com/en/comps/9/2024-2025/stats/players/2024-2025-Premier-League-Stats
    url = f"https://fbref.com/en/comps/{comp_code}/{season}/stats/players/{season}-Stats"
    r = requests.get(url, headers=HEADERS, timeout=30)
    if r.status_code != 200:
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", id="stats_standard")
    if not table:
        # some comps may name it differently, try 'stats_standard_dom_lg'
        table = soup.find("table", id="stats_standard_dom_lg")
        if not table:
            return []

    index = []
    for tr in table.select("tbody tr"):
        a = tr.find("a")
        if not a: 
            continue
        href = a.get("href","")
        # /en/players/{fbref_id}/player-name
        m = re.match(r"^/en/players/([a-zA-Z0-9]+)/", href)
        if not m:
            continue
        fb_id = m.group(1)
        name = a.text.strip()
        team_td = tr.find("td", {"data-stat":"team"})
        team = team_td.text.strip() if team_td else None
        # Some tables show duplicates per team; de-dupe later
        index.append({"fbref_id": fb_id, "name": name, "team": team})
    return index

def load_unmapped_players(conn):
    # load FPL players without FBREF mapping
    prov_id = conn.execute(text("SELECT id FROM external_providers WHERE code='FBREF'")).scalar_one()
    rows = conn.execute(text("""
        SELECT p.id AS player_id, p.name, t.short_name AS team
        FROM players p
        LEFT JOIN teams t ON t.id = p.team_id
        LEFT JOIN player_external_ids pei
          ON pei.player_id = p.id AND pei.provider_id = :prov
        WHERE pei.id IS NULL
        ORDER BY p.id
        LIMIT :lim OFFSET :off
    """), {"prov": prov_id, "lim": BATCH, "off": OFFSET}).mappings().all()
    return prov_id, rows

def main():
    eng = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
    with eng.begin() as conn:
        prov_id, targets = load_unmapped_players(conn)
        print(f"FBref mapping: {len(targets)} unmapped players (batch={BATCH}, offset={OFFSET})")

        # Build a global FBref index across comps/seasons (dedup by fbref_id, keep name/team seen last)
        fb_index = {}
        for comp in FBREF_COMPS:
            for season in SEASONS:
                time.sleep(SLEEP)
                try:
                    arr = fetch_comp_players(comp.strip(), season.strip())
                except Exception:
                    continue
                for r in arr:
                    fb_index[r["fbref_id"]] = r

        # Simple name/team matching
        by_name = {}
        for r in fb_index.values():
            key = (norm(r["name"]), norm(r["team"]))
            by_name.setdefault(key, []).append(r)

        upserts = 0
        for i, p in enumerate(targets, 1):
            key1 = (norm(p["name"]), norm(p["team"]))
            cands = by_name.get(key1, [])
            # fallback: match by name only
            if not cands:
                key2 = (norm(p["name"]), "")
                cands = by_name.get(key2, [])
            if not cands:
                print(f"[{i}/{len(targets)}] no FBref match: {p['name']} ({p['team'] or '-'})")
                continue

            cand = cands[0]
            # upsert
            conn.execute(text("""
              INSERT INTO player_external_ids(player_id, provider_id, external_id, matched_name, matched_team, confidence)
              VALUES (:pid, :prov, :ext, :mname, :mteam, :conf)
              ON CONFLICT (player_id, provider_id) DO UPDATE
                SET external_id = EXCLUDED.external_id,
                    matched_name = EXCLUDED.matched_name,
                    matched_team = EXCLUDED.matched_team,
                    confidence   = EXCLUDED.confidence,
                    updated_at   = NOW()
            """), {
                "pid": p["player_id"], "prov": prov_id, "ext": cand["fbref_id"],
                "mname": cand["name"], "mteam": cand["team"], "conf": 0.6  # mapping confidence heuristic
            })
            upserts += 1
            if i % 25 == 0:
                print(f"  …{i}/{len(targets)} mapped")

        print(f"FBref mapping upserts: {upserts}")

if __name__ == "__main__":
    main()
