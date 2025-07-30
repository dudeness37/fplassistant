# backend/scripts/export_unmapped_understat.py
import os
import pandas as pd
from sqlalchemy import create_engine, text

def main():
    db_url = os.environ["DATABASE_URL"]
    engine = create_engine(db_url, pool_pre_ping=True)

    query = """
    WITH prov AS (
      SELECT id
      FROM external_providers
      WHERE UPPER(code) = 'UNDERSTAT' OR LOWER(name) = 'understat'
      LIMIT 1
    )
    SELECT
      t.short_name AS team,
      p.id         AS player_id,
      p.name       AS player_name
    FROM players p
    LEFT JOIN teams t ON t.id = p.team_id
    LEFT JOIN player_external_ids pei
      ON pei.player_id = p.id
     AND pei.provider_id = (SELECT id FROM prov)
    WHERE pei.id IS NULL
    ORDER BY team, player_name;
    """
    df = pd.read_sql(text(query), engine)
    out_dir = "/app/tmp"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/unmapped_understat.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path} rows={len(df)}")

if __name__ == "__main__":
    main()
