# backend/scripts/map_understat_ids.py
import os
import re
import json
import time
import unicodedata
from typing import Dict, List, Tuple, Optional

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError, ProgrammingError

# ----------------------------
# Config via environment
# ----------------------------
DATABASE_URL      = os.environ.get("DATABASE_URL")
US_LEAGUES        = os.environ.get("US_LEAGUES", "EPL,La_Liga,Serie_A,Bundesliga,Ligue_1")
US_SEASONS        = os.environ.get("US_SEASONS", "2024,2023,2022")
RETRY_ATTEMPTS    = int(os.environ.get("RETRY_ATTEMPTS", "1"))  # default: 1 (no real backoff)
RETRY_BACKOFF     = float(os.environ.get("RETRY_BACKOFF", "1.0"))
BATCH             = int(os.environ.get("BATCH", "300"))
OFFSET            = int(os.environ.get("OFFSET", "0"))

# provider code/name we will use
PROVIDER_CODE     = "UNDERSTAT"
PROVIDER_NAME     = "understat"

# ----------------------------
# Helpers
# ----------------------------
def normalize(s: str) -> str:
    if not s:
        return ""
    s = s.strip()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-zA-Z0-9\s\-']", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()

def token_set(s: str) -> set:
    return set(normalize(s).replace("-", " ").split())

def name_similarity(a: str, b: str) -> float:
    ta, tb = token_set(a), token_set(b)
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter / union if union else 0.0

EPL_TEAM_NAMES = {
    "ARS": {"arsenal"},
    "MCI": {"manchester city", "man city"},
    "MUN": {"manchester united", "man united", "man utd"},
    "NEW": {"newcastle united", "newcastle"},
    "CHE": {"chelsea"},
    "LIV": {"liverpool"},
    "TOT": {"tottenham", "tottenham hotspur", "spurs"},
    "AVL": {"aston villa"},
    "BHA": {"brighton", "brighton hove albion", "brighton & hove albion"},
    "WHU": {"west ham united", "west ham"},
    "BRE": {"brentford"},
    "CRY": {"crystal palace"},
    "FUL": {"fulham"},
    "EVE": {"everton"},
    "NFO": {"nottingham forest", "nottm forest", "nottingham"},
    "WOL": {"wolverhampton wanderers", "wolves"},
    "LEI": {"leicester city", "leicester"},
    "IPS": {"ipswich town", "ipswich"},
    "SOU": {"southampton"},
    "BOU": {"afc bournemouth", "bournemouth"},
    # add others if promoted/changed in your DB
}

def team_name_matches(fpl_short: Optional[str], understat_team: Optional[str]) -> bool:
    if not fpl_short or not understat_team:
        return False
    want = EPL_TEAM_NAMES.get(fpl_short, set())
    tnorm = normalize(understat_team)
    return any(tnorm == x or x in tnorm for x in want)

def fetch_understat_league_players(league: str, season: str) -> List[Dict]:
    """
    Returns list of dicts with understat players for given league/season.
    Skips 404 immediately; retries only for non-404 transient errors (per RETRY_ATTEMPTS).
    """
    url = f"https://understat.com/league/{league}/{season}"
    for i in range(RETRY_ATTEMPTS):
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 404:
                print(f"Skip {league} {season}: 404 Not Found")
                return []
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            script = None
            for s in soup.find_all("script"):
                if s.string and "playersData" in s.string:
                    script = s.string
                    break
            if not script:
                return []
            m = re.search(r"playersData\s*=\s*JSON\.parse\('(.+?)'\)", script)
            if not m:
                return []
            raw = m.group(1).encode("utf-8").decode("unicode_escape")
            data = json.loads(raw)  # list of dicts
            return data
        except requests.HTTPError as e:
            if i == RETRY_ATTEMPTS - 1:
                print(f"Fetch {league} {season}: {e} — giving up")
                return []
            back = RETRY_BACKOFF * (2 ** i)
            print(f"[retry {i+1}/{RETRY_ATTEMPTS}] {e} — sleeping {back}s")
            time.sleep(back)
        except Exception as e:
            if i == RETRY_ATTEMPTS - 1:
                print(f"Fetch {league} {season}: {e} — giving up")
                return []
            back = RETRY_BACKOFF * (2 ** i)
            print(f"[retry {i+1}/{RETRY_ATTEMPTS}] {e} — sleeping {back}s")
            time.sleep(back)
    return []

def build_understat_index(leagues: List[str], seasons: List[str]) -> Dict[str, Dict]:
    """
    Build dict: key = normalized player_name, value = dict of best candidate per name:
      {
        '<norm-name>': {
           'understat_id': str,
           'player_name': str,
           'team_title': str
        }
      }
    If multiple entries for a name across seasons/teams, we keep the last seen (good enough for mapping).
    """
    idx: Dict[str, Dict] = {}
    for lg in leagues:
        for yr in seasons:
            players = fetch_understat_league_players(lg, yr)
            if not players:
                continue
            for p in players:
                pid = str(p.get("id") or "").strip()
                pname = (p.get("player_name") or "").strip()
                tname = (p.get("team_title") or "").strip()
                if not pid or not pname:
                    continue
                key = normalize(pname)
                idx[key] = {
                    "understat_id": pid,
                    "player_name": pname,
                    "team_title": tname
                }
    return idx

def table_has_column(conn, table: str, column: str) -> bool:
    q = text("""
      SELECT 1
      FROM information_schema.columns
      WHERE table_schema='public' AND table_name=:t AND column_name=:c
      LIMIT 1
    """)
    return conn.execute(q, {"t": table, "c": column}).scalar() is not None

def unique_exists(conn, relname: str, conname: str) -> bool:
    q = text("""
      SELECT 1
      FROM pg_constraint
      WHERE conname = :conname
        AND conrelid = :relname::regclass
      LIMIT 1
    """)
    return conn.execute(q, {"conname": conname, "relname": relname}).scalar() is not None

# ----------------------------
# Main
# ----------------------------
def main():
    if not DATABASE_URL:
        raise SystemExit("DATABASE_URL not set")

    leagues = [x.strip() for x in US_LEAGUES.split(",") if x.strip()]
    seasons = [x.strip() for x in US_SEASONS.split(",") if x.strip()]

    print("Mapping Understat IDs for FPL players…")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    with engine.begin() as conn:
        # Ensure provider row exists (either code or name unique)
        # Try by code first, fallback to name
        prov_id = conn.execute(text("""
          SELECT id FROM external_providers
          WHERE UPPER(code) = :c OR LOWER(name) = :n
          LIMIT 1
        """), {"c": PROVIDER_CODE, "n": PROVIDER_NAME}).scalar()

        if prov_id is None:
            # Try insert by code
            try:
                prov_id = conn.execute(text("""
                  INSERT INTO external_providers(code, name)
                  VALUES (:c, :n)
                  ON CONFLICT (code) DO NOTHING
                  RETURNING id
                """), {"c": PROVIDER_CODE, "n": PROVIDER_NAME}).scalar()
            except ProgrammingError:
                # If unique is on name not code
                prov_id = conn.execute(text("""
                  INSERT INTO external_providers(name, code)
                  VALUES (:n, :c)
                  ON CONFLICT (name) DO NOTHING
                  RETURNING id
                """), {"c": PROVIDER_CODE, "n": PROVIDER_NAME}).scalar()

            if prov_id is None:
                # fetch existing now
                prov_id = conn.execute(text("""
                  SELECT id FROM external_providers
                  WHERE UPPER(code) = :c OR LOWER(name) = :n
                  LIMIT 1
                """), {"c": PROVIDER_CODE, "n": PROVIDER_NAME}).scalar()

        # Figure out which optional columns we can write to
        has_mname   = table_has_column(conn, "player_external_ids", "matched_name")
        has_mteam   = table_has_column(conn, "player_external_ids", "matched_team")
        has_conf    = table_has_column(conn, "player_external_ids", "confidence")
        has_upd     = table_has_column(conn, "player_external_ids", "updated_at")

        # Load unmapped players for this provider (paged)
        players = conn.execute(text("""
            SELECT p.id, p.name, t.short_name AS team_short
            FROM players p
            LEFT JOIN teams t ON t.id = p.team_id
            LEFT JOIN player_external_ids pei
              ON pei.player_id = p.id AND pei.provider_id = :prov
            WHERE pei.id IS NULL
            ORDER BY p.id
            LIMIT :batch OFFSET :off
        """), {"prov": prov_id, "batch": BATCH, "off": OFFSET}).mappings().all()

    print(f"…loaded {len(players)} unmapped players (batch={BATCH}, offset={OFFSET})")

    # Build Understat index once
    us_idx = build_understat_index(leagues, seasons)

    mapped = 0
    updated = 0
    skipped = 0

    with engine.begin() as conn:
        for i, row in enumerate(players, start=1):
            pid   = int(row["id"])
            pname = row["name"] or ""
            pteam = row["team_short"]

            # find a candidate
            key = normalize(pname)
            cand = us_idx.get(key)

            chosen_id = None
            m_team    = None
            conf      = 0.0

            # Strategy:
            # 1) exact normalized name hit: boost confidence, check team
            # 2) if not, scan nearby names by token similarity (>0.7)
            if cand:
                chosen_id = cand["understat_id"]
                m_team    = cand.get("team_title") or ""
                conf      = 1.0 if team_name_matches(pteam, m_team) else 0.8
            else:
                # fallback: nearest by Jaccard token similarity
                best = (0.0, None)
                for k, v in us_idx.items():
                    sim = name_similarity(pname, v["player_name"])
                    if sim > best[0]:
                        best = (sim, v)
                if best[0] >= 0.7 and best[1] is not None:
                    v = best[1]
                    chosen_id = v["understat_id"]
                    m_team    = v.get("team_title") or ""
                    conf      = 0.6 if not team_name_matches(pteam, m_team) else 0.75

            if not chosen_id:
                print(f"[{i}/{len(players)}] no match: {pname} ({pteam or '-'})")
                skipped += 1
                continue

            # Build parameter dict for write
            params = {
                "player_id": pid,
                "prov_id":   prov_id,
                "external_id": str(chosen_id),
            }
            if has_mname:
                params["mname"] = pname
            if has_mteam:
                params["mteam"] = (m_team or "")
            if has_conf:
                params["conf"]  = conf

            # 1) Try UPDATE first (safe even if unique on (provider_id, external_id) exists)
            set_cols = ["external_id = :external_id"]
            if has_mname: set_cols.append("matched_name = :mname")
            if has_mteam: set_cols.append("matched_team = :mteam")
            if has_conf:  set_cols.append("confidence = :conf")
            if has_upd:   set_cols.append("updated_at = NOW()")

            upd_sql = f"""
                UPDATE player_external_ids
                   SET {", ".join(set_cols)}
                 WHERE player_id = :player_id
                   AND provider_id = :prov_id
            """
            r = conn.execute(text(upd_sql), params)

            if r.rowcount and r.rowcount > 0:
                print(f"[{i}/{len(players)}] updated: {pname} -> understat_id {chosen_id} (conf={conf:.2f})")
                updated += 1
                continue

            # 2) INSERT if no row existed for (player_id, provider_id)
            cols = ["player_id", "provider_id", "external_id"]
            vals = [":player_id", ":prov_id", ":external_id"]
            if has_mname:
                cols.append("matched_name"); vals.append(":mname")
            if has_mteam:
                cols.append("matched_team"); vals.append(":mteam")
            if has_conf:
                cols.append("confidence");   vals.append(":conf")

            ins_sql = f"""
                INSERT INTO player_external_ids({", ".join(cols)})
                VALUES ({", ".join(vals)})
            """
            try:
                conn.execute(text(ins_sql), params)
                print(f"[{i}/{len(players)}] mapped: {pname} -> understat_id {chosen_id} (conf={conf:.2f})")
                mapped += 1
            except IntegrityError as e:
                # Most likely unique(provider_id, external_id) exists for someone else.
                print(f"[{i}/{len(players)}] duplicate understat_id {chosen_id} for provider; keeping existing row. ({pname})")
                skipped += 1

    print(f"Done. mapped={mapped}, updated={updated}, skipped={skipped}")
    print("Tip: run next batch with OFFSET incremented, e.g., OFFSET={}".format(OFFSET + BATCH))

if __name__ == "__main__":
    main()
