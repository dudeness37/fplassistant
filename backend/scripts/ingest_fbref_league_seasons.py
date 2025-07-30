import os
import re
import time
import unicodedata
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
from sqlalchemy import create_engine, text

DB_URL = os.environ["DATABASE_URL"]

# Input via env (comma-separated)
LEAGUES = [s.strip() for s in os.getenv("FBREF_LEAGUES", "9").split(",") if s.strip()]
SEASONS = [s.strip() for s in os.getenv("FBREF_SEASONS", "2023-2024").split(",") if s.strip()]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Referer": "https://fbref.com/en/",
    "DNT": "1",
    "Connection": "keep-alive",
}

LEAGUE_CODE_TO_NAME = {
    "9":  "Premier-League",
    "12": "La-Liga",
    "11": "Serie-A",
    "20": "Bundesliga",
    "13": "Ligue-1",       # (FBref sometimes uses 'Ligue-1' or 'Ligue 1'; this path uses hyphen)
    "24": "Primeira-Liga",
    "10": "Eredivisie",
    "32": "Championship",
}

# FBref season slug -> store as "YYYY/YY"
def season_slug_to_label(slug: str) -> str:
    # '2023-2024' -> '2023/24'
    m = re.match(r"^(\d{4})-(\d{4})$", slug)
    if not m:
        return slug
    start = m.group(1)
    end2 = m.group(2)[2:]
    return f"{start}/{end2}"

def normalize_text(s: str) -> str:
    if s is None:
        return ""
    s = s.strip()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s

def fetch_fbref_standard_table(league_code: str, season_slug: str) -> pd.DataFrame | None:
    league_name = LEAGUE_CODE_TO_NAME.get(league_code, league_code)
    # Example: https://fbref.com/en/comps/9/2023-2024/stats/players/2023-2024-Premier-League-Stats
    url = f"https://fbref.com/en/comps/{league_code}/{season_slug}/stats/players/{season_slug}-{league_name}-Stats"

    # 1) Fetch HTML with headers
    r = requests.get(url, headers=HEADERS, timeout=25)
    if r.status_code == 403:
        # try one retry with a short sleep
        time.sleep(1.0)
        r = requests.get(url, headers=HEADERS, timeout=25)
    r.raise_for_status()

    html = r.text
    soup = BeautifulSoup(html, "lxml")

    # 2) FBref often comments out the table. Search comments for a table with id='stats_standard'
    def extract_table_from_soup(s: BeautifulSoup) -> str | None:
        # try direct
        tbl = s.find("table", id="stats_standard")
        if tbl:
            return str(tbl)

        # try commented sections
        for c in s.find_all(string=lambda text: isinstance(text, Comment)):
            try:
                inner = BeautifulSoup(c, "lxml")
                itbl = inner.find("table", id="stats_standard")
                if itbl:
                    return str(itbl)
            except Exception:
                continue
        return None

    table_html = extract_table_from_soup(soup)
    if not table_html:
        print(f"[{season_slug}:{league_name}] No usable table found; skipping")
        return None

    # 3) Parse with pandas
    try:
        df_list = pd.read_html(StringIO(table_html))
        if not df_list:
            return None
        df = df_list[0]
    except ValueError:
        return None

    # 4) Standardize column names we care about
    df.columns = [str(c).strip() for c in df.columns]
    # Common columns on FBref standard table:
    # 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', 'MP', 'Starts',
    # 'Min', 'Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR', 'xG', 'npxG', 'xAG',
    # 'xG+xAG', 'npxG+xAG', 'PrgC', 'PrgP', 'PrgR', 'Gls', etc.

    # Deduplicate header rows (FBref repeats headers inside the table)
    if "Rk" in df.columns:
        df = df[df["Rk"].astype(str).str.isnumeric()]

    # Keep minimal set
    keep = {
        "Player": "player_name",
        "Squad": "team_name",
        "Pos": "pos",
        "Min": "minutes",
        "Gls": "goals",
        "Ast": "assists",
        "Sh": "shots",
        "SoT": "shots_on_target",
        "xG": "xg",
        "xAG": "xa",
        "npxG": "npxg",
        "npxG+xAG": "npxg_xa",
    }
    present = {src: keep[src] for src in keep.keys() if src in df.columns}
    df = df[list(present.keys())].rename(columns=present)
    df["player_name"] = df["player_name"].apply(normalize_text)
    df["team_name"] = df["team_name"].apply(normalize_text)

    # cast numerics
    for col in ["minutes", "goals", "assists", "shots", "shots_on_target", "xg", "xa", "npxg", "npxg_xa"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # add season label and comp name for storage
    df["season"] = season_slug_to_label(season_slug)
    df["comp"] = league_name.replace("-", " ")

    return df

def ensure_provider_fbref(conn) -> int:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS external_providers (
          id   BIGSERIAL PRIMARY KEY,
          code TEXT UNIQUE NOT NULL,
          name TEXT
        );
    """))
    row = conn.execute(text("SELECT id FROM external_providers WHERE UPPER(code)='FBREF'")).first()
    if row:
        return int(row[0])
    row = conn.execute(text("INSERT INTO external_providers(code, name) VALUES ('FBREF','FBref') RETURNING id")).first()
    return int(row[0])

def ensure_external_player_seasons_shape(conn):
    conn.execute(text("""
      CREATE TABLE IF NOT EXISTS external_player_seasons (
        id BIGSERIAL PRIMARY KEY,
        player_id INT REFERENCES players(id),
        provider_id INT REFERENCES external_providers(id),
        season TEXT,
        team TEXT,
        comp TEXT,
        minutes NUMERIC,
        goals NUMERIC,
        assists NUMERIC,
        shots NUMERIC,
        key_passes NUMERIC,
        xg NUMERIC,
        xa NUMERIC,
        npxg NUMERIC,
        npxg_xa NUMERIC,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
      );
    """))
    # Unique key to upsert safely
    conn.execute(text("""
      DO $$
      BEGIN
        IF NOT EXISTS (
          SELECT 1 FROM pg_constraint
          WHERE conname='uq_eps_player_provider_season_team_comp'
            AND conrelid='external_player_seasons'::regclass
        ) THEN
          ALTER TABLE external_player_seasons
          ADD CONSTRAINT uq_eps_player_provider_season_team_comp
          UNIQUE (player_id, provider_id, season, COALESCE(team, ''), COALESCE(comp,''));
        END IF;
      END$$;
    """))

def build_team_map(conn) -> dict[str, int]:
    # Map FBref team -> teams.id using teams.name or teams.short_name heuristics
    rows = conn.execute(text("SELECT id, name, short_name FROM teams")).mappings().all()
    mp = {}
    for r in rows:
        names = {normalize_text(r["name"]), normalize_text(r["short_name"])}
        for n in list(names):
            # Some FBref styles: 'Manchester City' vs 'Man City'
            names.add(n.replace("Manchester United", "Man United"))
            names.add(n.replace("Manchester City", "Man City"))
            names.add(n.replace("Brighton and Hove Albion", "Brighton"))
            names.add(n.replace("Wolverhampton Wanderers", "Wolves"))
        for n in names:
            if n:
                mp[n] = r["id"]
    return mp

def find_player_id(conn, player_name: str, team_id: int | None) -> int | None:
    # Try exact by name; if multiple, prefer matching team_id
    q = text("""
      SELECT id, team_id FROM players
      WHERE name = :n
    """)
    cand = conn.execute(q, {"n": player_name}).fetchall()
    if not cand:
        return None
    if team_id is None:
        return cand[0][0]
    # choose by team match if possible
    for pid, tid in cand:
        if tid == team_id:
            return pid
    return cand[0][0]

def main():
    engine = create_engine(DB_URL, pool_pre_ping=True)

    print(f"FBref ingest: leagues={LEAGUES}, seasons={SEASONS}")

    total_upserts = 0
    with engine.begin() as conn:
        prov_id = ensure_provider_fbref(conn)
        ensure_external_player_seasons_shape(conn)
        team_map = build_team_map(conn)

    for season in SEASONS:
        for lg in LEAGUES:
            df = fetch_fbref_standard_table(lg, season)
            if df is None or df.empty:
                continue

            with engine.begin() as conn:
                up = 0
                for _, row in df.iterrows():
                    team_name = row.get("team_name", "")
                    player_name = row.get("player_name", "")
                    if not player_name:
                        continue

                    # resolve team_id using heuristics
                    team_id = None
                    tnorm = normalize_text(team_name)
                    if tnorm in team_map:
                        team_id = team_map[tnorm]
                    else:
                        # fallback: try a few common replacements
                        t2 = (tnorm
                              .replace("Man United", "MUN")
                              .replace("Man City", "MCI")
                              .replace("Brighton", "BHA")
                              .replace("Wolves", "WOL"))
                        # This only helps if teams.short_name are used; otherwise remain None

                    # find player_id
                    pid = find_player_id(conn, player_name, team_id)

                    # only store if we can map to a player_id (we’re filling FPL player history)
                    if pid is None:
                        continue

                    params = {
                        "player_id": pid,
                        "prov_id": prov_id,
                        "season": row["season"],
                        "team": team_name,
                        "comp": row.get("comp", ""),
                        "minutes": float(row.get("minutes", 0) or 0),
                        "goals": float(row.get("goals", 0) or 0),
                        "assists": float(row.get("assists", 0) or 0),
                        "shots": float(row.get("shots", 0) or 0),
                        "key_passes": float(row.get("shots_on_target", 0) or 0),  # FBref 'SoT' -> we can map to 'key_passes' only if present; if not, keep 0
                        "xg": float(row.get("xg", 0) or 0),
                        "xa": float(row.get("xa", 0) or 0),
                        "npxg": float(row.get("npxg", 0) or 0),
                        "npxg_xa": float(row.get("npxg_xa", 0) or 0),
                    }

                    # Prefer UPDATE then INSERT (idempotent)
                    upd = conn.execute(text("""
                        UPDATE external_player_seasons
                        SET team=:team, comp=:comp, minutes=:minutes, goals=:goals, assists=:assists,
                            shots=:shots, key_passes=:key_passes, xg=:xg, xa=:xa, npxg=:npxg, npxg_xa=:npxg_xa,
                            updated_at=NOW()
                        WHERE player_id=:player_id AND provider_id=:prov_id
                          AND season=:season AND COALESCE(team,'')=COALESCE(:team,'')
                          AND COALESCE(comp,'')=COALESCE(:comp,'')
                    """), params)

                    if upd.rowcount == 0:
                        conn.execute(text("""
                            INSERT INTO external_player_seasons
                              (player_id, provider_id, season, team, comp,
                               minutes, goals, assists, shots, key_passes,
                               xg, xa, npxg, npxg_xa, created_at, updated_at)
                            VALUES
                              (:player_id, :prov_id, :season, :team, :comp,
                               :minutes, :goals, :assists, :shots, :key_passes,
                               :xg, :xa, :npxg, :npxg_xa, NOW(), NOW())
                        """), params)
                        up += 1

                total_upserts += up
                print(f"[{season}:{LEAGUE_CODE_TO_NAME.get(lg, lg)}] upserted≈{up}")

            # small politeness delay
            time.sleep(0.4)

    print(f"FBref seasons ingest ✓ total rows upserted≈{total_upserts}")

if __name__ == "__main__":
    main()
