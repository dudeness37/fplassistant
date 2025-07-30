# /app/scripts/ingest_fbref_seasons.py
import os, time, re
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; fpl-ai-ingest/1.0; +https://github.com/dudeness37/fplassistant)"
}
SLEEP = float(os.environ.get("SLEEP", "0.8"))
MAX_PLAYERS = int(os.environ.get("MAX_PLAYERS", "800"))

def fetch_player_seasons(fbref_id: str):
    # Player page: https://fbref.com/en/players/{id}/
    url = f"https://fbref.com/en/players/{fbref_id}/"
    r = requests.get(url, headers=HEADERS, timeout=30)
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    # Prefer the "Standard" and "Expected" tables at the player summary (Career)
    tables = soup.find_all("table")
    seasons = {}  # season -> aggregate dict

    def parse_num(x):
        try:
            return int(x.replace(",", ""))
        except:
            try:
                return float(x.replace(",",""))
            except:
                return None

    # Standard stats by season (league rows)
    for tbl in tables:
        if not tbl.get("id","").startswith("stats_standard_"):
            continue
        for tr in tbl.select("tbody tr"):
            if tr.get("class") and "thead" in tr.get("class"): 
                continue
            season = tr.find("th", {"data-stat":"season"})
            comp = tr.find("td", {"data-stat":"comp_level"})
            team = tr.find("td", {"data-stat":"team"})
            if not (season and comp and team):
                continue
            season_txt = season.text.strip()
            league = comp.text.strip()
            team_name = team.text.strip()
            minutes = tr.find("td", {"data-stat":"minutes"})
            matches = tr.find("td", {"data-stat":"games"})
            starts  = tr.find("td", {"data-stat":"games_starts"})
            goals   = tr.find("td", {"data-stat":"goals"})
            assists = tr.find("td", {"data-stat":"assists"})
            row = seasons.setdefault((season_txt, league, team_name), {})
            row["minutes"] = (row.get("minutes") or 0) + (parse_num(minutes.text) if minutes else 0)
            row["matches"] = (row.get("matches") or 0) + (parse_num(matches.text) if matches else 0)
            row["starts"]  = (row.get("starts")  or 0) + (parse_num(starts.text)  if starts  else 0)
            row["goals"]   = (row.get("goals")   or 0) + (parse_num(goals.text)   if goals   else 0)
            row["assists"] = (row.get("assists") or 0) + (parse_num(assists.text) if assists else 0)

    # Expected (xG/xA) by season (if available)
    for tbl in tables:
        if not tbl.get("id","").startswith("stats_expected_"):
            continue
        for tr in tbl.select("tbody tr"):
            if tr.get("class") and "thead" in tr.get("class"): 
                continue
            season = tr.find("th", {"data-stat":"season"})
            comp = tr.find("td", {"data-stat":"comp_level"})
            team = tr.find("td", {"data-stat":"team"})
            if not (season and comp and team):
                continue
            season_txt = season.text.strip()
            league = comp.text.strip()
            team_name = team.text.strip()
            xg  = tr.find("td", {"data-stat":"xg"})
            xa  = tr.find("td", {"data-stat":"xa"})
            npxg= tr.find("td", {"data-stat":"npxg"})
            key = (season_txt, league, team_name)
            row = seasons.setdefault(key, {})
            if xg:  row["xg"]  = float(xg.text)  if xg.text.strip()  else row.get("xg")
            if xa:  row["xa"]  = float(xa.text)  if xa.text.strip()  else row.get("xa")
            if npxg:row["npxg"]= float(npxg.text)if npxg.text.strip() else row.get("npxg")

    # flatten
    out = []
    for (season_txt, league, team_name), v in seasons.items():
        out.append({
            "season": season_txt, "league": league, "team_name": team_name,
            "minutes": v.get("minutes"), "matches": v.get("matches"),
            "starts": v.get("starts"), "goals": v.get("goals"), "assists": v.get("assists"),
            "xg": v.get("xg"), "xa": v.get("xa"), "npxg": v.get("npxg"),
        })
    return out

def main():
    eng = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
    with eng.begin() as conn:
        prov_id = conn.execute(text("SELECT id FROM external_providers WHERE code='FBREF'")).scalar_one()
        rows = conn.execute(text("""
          SELECT p.id AS player_id, pei.external_id
          FROM players p
          JOIN player_external_ids pei
            ON pei.player_id = p.id AND pei.provider_id = :prov
          ORDER BY p.id
          LIMIT :lim
        """), {"prov": prov_id, "lim": MAX_PLAYERS}).mappings().all()

        print(f"Ingest FBref seasons for {len(rows)} players (max={MAX_PLAYERS})")
        upserts = 0
        for i, r in enumerate(rows, 1):
            time.sleep(SLEEP)
            try:
                data = fetch_player_seasons(r["external_id"])
            except Exception as e:
                print(f"[{i}/{len(rows)}] FBref fetch failed: {e}")
                continue
            for d in data:
                conn.execute(text("""
                  INSERT INTO external_player_seasons
                    (player_id, provider_id, season, league, team_name, minutes, matches, starts, goals, assists, xg, xa, npxg)
                  VALUES
                    (:pid, :prov, :season, :league, :team, :minutes, :matches, :starts, :goals, :assists, :xg, :xa, :npxg)
                  ON CONFLICT (player_id, provider_id, season, league, team_name)
                  DO UPDATE SET
                    minutes = EXCLUDED.minutes,
                    matches = EXCLUDED.matches,
                    starts  = EXCLUDED.starts,
                    goals   = EXCLUDED.goals,
                    assists = EXCLUDED.assists,
                    xg      = EXCLUDED.xg,
                    xa      = EXCLUDED.xa,
                    npxg    = EXCLUDED.npxg,
                    updated_at = NOW()
                """), {
                    "pid": r["player_id"], "prov": prov_id,
                    "season": d["season"], "league": d["league"], "team": d["team_name"],
                    "minutes": d["minutes"], "matches": d["matches"], "starts": d["starts"],
                    "goals": d["goals"], "assists": d["assists"],
                    "xg": d["xg"], "xa": d["xa"], "npxg": d["npxg"]
                })
                upserts += 1

            if i % 25 == 0:
                print(f"  …{i}/{len(rows)} players ingested")
        print(f"FBref season rows upserted: {upserts}")

if __name__ == "__main__":
    main()
