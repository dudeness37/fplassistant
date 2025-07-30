# /app/scripts/patch_unmapped_priors.py
import os
from sqlalchemy import create_engine, text

PRIOR_CODE = "PRIOR"

PRIOR_DEFAULTS = {
    # Conservative “good enough” priors if no FPL GW rows exist
    "minutes": 900,     # ~10 full matches
    "matches": 15,
    "starts":  10,
    "goals":   None,    # we don't have FPL goals in gw table; leave null
    "assists": None,    # same here
    "xg":      2.0,
    "xa":      1.5,
    "npxg":    1.8,
    "shots":   None,
    "key_passes": None,
}

SQL_FIND_UNMAPPED = """
WITH us AS (
  SELECT player_id FROM player_external_ids pei
  JOIN external_providers ep ON ep.id = pei.provider_id
  WHERE ep.code = 'UNDERSTAT'
),
fb AS (
  SELECT player_id FROM player_external_ids pei
  JOIN external_providers ep ON ep.id = pei.provider_id
  WHERE ep.code = 'FBREF'
)
SELECT p.id AS player_id
FROM players p
LEFT JOIN us ON us.player_id = p.id
LEFT JOIN fb ON fb.player_id = p.id
WHERE us.player_id IS NULL AND fb.player_id IS NULL
ORDER BY p.id
"""

# Use latest season we do have in player_gw_stats to build a better prior
SQL_LATEST_AGG = """
WITH latest AS (
  SELECT player_id, MAX(season) AS season
  FROM player_gw_stats
  GROUP BY player_id
),
agg AS (
  SELECT s.player_id,
         SUM(COALESCE(s.minutes,0))     AS minutes,
         COUNT(*)                        AS matches,
         SUM(CASE WHEN COALESCE(s.minutes,0) >= 60 THEN 1 ELSE 0 END) AS starts,
         SUM(COALESCE(s.xG,0))          AS xg,
         SUM(COALESCE(s.xA,0))          AS xa,
         SUM(COALESCE(s.xG,0))          AS npxg,    -- no NP split; use xG as proxy
         SUM(COALESCE(s.shots,0))       AS shots,
         SUM(COALESCE(s.key_passes,0))  AS key_passes
  FROM player_gw_stats s
  JOIN latest l ON l.player_id = s.player_id AND l.season = s.season
  GROUP BY s.player_id
)
SELECT * FROM agg WHERE player_id = :pid
"""

SQL_UPSERT_PRIOR = """
INSERT INTO external_player_seasons
  (player_id, provider_id, season, league, team_name,
   minutes, matches, starts, goals, assists, xg, xa, npxg, shots, key_passes)
VALUES
  (:pid, :prov, 'PRIOR', 'PRIOR', 'PRIOR',
   :minutes, :matches, :starts, :goals, :assists, :xg, :xa, :npxg, :shots, :key_passes)
ON CONFLICT (player_id, provider_id, season, league, team_name)
DO UPDATE SET
  minutes = COALESCE(EXCLUDED.minutes, external_player_seasons.minutes),
  matches = COALESCE(EXCLUDED.matches, external_player_seasons.matches),
  starts  = COALESCE(EXCLUDED.starts,  external_player_seasons.starts),
  goals   = COALESCE(EXCLUDED.goals,   external_player_seasons.goals),
  assists = COALESCE(EXCLUDED.assists, external_player_seasons.assists),
  xg      = COALESCE(EXCLUDED.xg,      external_player_seasons.xg),
  xa      = COALESCE(EXCLUDED.xa,      external_player_seasons.xa),
  npxg    = COALESCE(EXCLUDED.npxg,    external_player_seasons.npxg),
  shots   = COALESCE(EXCLUDED.shots,   external_player_seasons.shots),
  key_passes = COALESCE(EXCLUDED.key_passes, external_player_seasons.key_passes),
  updated_at = NOW()
"""

def main():
    eng = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)

    with eng.begin() as c:
        # 1) Ensure PRIOR provider exists; get ids
        prov_prior = c.execute(text("SELECT id FROM external_providers WHERE code=:c"), {"c": PRIOR_CODE}).scalar()
        if not prov_prior:
            # create if missing
            c.execute(text("INSERT INTO external_providers(code, name) VALUES (:c, :n) ON CONFLICT (code) DO NOTHING"),
                      {"c": PRIOR_CODE, "n": "fallback priors"})
            prov_prior = c.execute(text("SELECT id FROM external_providers WHERE code=:c"), {"c": PRIOR_CODE}).scalar()

        # 2) Who is still unmapped to both Understat and FBref?
        unmapped = [r for (r,) in c.execute(text(SQL_FIND_UNMAPPED)).all()]
        print(f"Unmapped players (no Understat & no FBref): {len(unmapped)}")

        inserted = 0
        updated  = 0

        for pid in unmapped:
            # Try to derive better priors from latest FPL GW season if available
            row = c.execute(text(SQL_LATEST_AGG), {"pid": pid}).mappings().one_or_none()
            vals = dict(PRIOR_DEFAULTS)  # copy defaults
            if row:
                # prefer real aggregates when present
                vals.update({
                    "minutes":    int(row["minutes"] or 0),
                    "matches":    int(row["matches"] or 0),
                    "starts":     int(row["starts"]  or 0),
                    "xg":         float(row["xg"]    or 0) if row["xg"] is not None else None,
                    "xa":         float(row["xa"]    or 0) if row["xa"] is not None else None,
                    "npxg":       float(row["npxg"]  or 0) if row["npxg"] is not None else None,
                    "shots":      int(row["shots"]   or 0) if row["shots"] is not None else None,
                    "key_passes": int(row["key_passes"] or 0) if row["key_passes"] is not None else None,
                    # goals/assists unknown in gw table -> remain None
                })

            r = c.execute(text(SQL_UPSERT_PRIOR), {
                "pid": pid, "prov": prov_prior,
                **{k: vals.get(k) for k in ["minutes","matches","starts","goals","assists","xg","xa","npxg","shots","key_passes"]}
            })
            # rowcount can be 0 on no-op updates; we don't strictly rely on it
            if r.rowcount and r.rowcount > 0:
                # On insert rowcount==1 (in PG) or update rowcount==1; treat both as “written”
                inserted += 1

        print(f"PRIOR rows written (inserted/updated): {inserted}")

if __name__ == "__main__":
    main()
