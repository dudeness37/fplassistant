# app/services/scheduler.py
import os
import datetime as dt
from zoneinfo import ZoneInfo

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# We will import our loaders as modules
from scripts import bootstrap_upsert, load_fixtures, load_player_history_vaastav
from scripts import map_understat_ids, ingest_understat_seasons

TZ = ZoneInfo("Europe/Madrid")

async def refresh_all():
    """
    Full refresh (idempotent): FPL bootstrap, fixtures, current season history,
    Understat mapping and last few seasons ingestion.
    """
    print("[scheduler] refresh_all: start")
    # 1) FPL bootstrap (teams/players)
    bootstrap_upsert.main()

    # 2) Fixtures
    load_fixtures.main()

    # 3) Player GW history for current season (FPL). Adjust season here if needed.
    season = os.getenv("CURRENT_SEASON", "2024/25")
    os.environ["SEASON"] = season
    # If you loaded historical seasons separately, here we only keep current season up-to-date.
    load_player_history_vaastav.main()

    # 4) Understat mapping + last N seasons
    map_understat_ids.main()
    ingest_understat_seasons.main()

    print("[scheduler] refresh_all: done")

async def within_burst_window() -> bool:
    """
    Use the official FPL bootstrap to locate next deadline and see if within 6h.
    """
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get("https://fantasy.premierleague.com/api/bootstrap-static/")
            r.raise_for_status()
            data = r.json()
        next_ev = next((e for e in data["events"] if not e.get("finished") and e.get("deadline_time")), None)
        if not next_ev:
            return False
        dl = dt.datetime.fromisoformat(next_ev["deadline_time"].replace("Z", "+00:00")).astimezone(TZ)
        now = dt.datetime.now(TZ)
        return dt.timedelta(0) <= (dl - now) <= dt.timedelta(hours=6)
    except Exception as e:
        print("[scheduler] within_burst_window error:", e)
        return False

async def burst_job():
    if await within_burst_window():
        print("[scheduler] burst window active → running refresh_all()")
        await refresh_all()
    else:
        # no-op
        pass

def start_scheduler():
    sched = AsyncIOScheduler(timezone=str(TZ))

    # Twice daily strong refresh
    sched.add_job(refresh_all, "cron", hour="9,21", minute=0, id="twice_daily_refresh")

    # Every 30 minutes, run burst job if within 6 hours of deadline
    sched.add_job(burst_job, "cron", minute="*/30", id="deadline_burst")

    # Optional: quick daily Understat-only refresh at 03:00
    # sched.add_job(map_understat_ids.main, "cron", hour=3, minute=0, id="understat_map_daily")
    # sched.add_job(ingest_understat_seasons.main, "cron", hour=3, minute=15, id="understat_ingest_daily")

    sched.start()
    print("[scheduler] started")

# Utility for testing: schedule a one-time run at a given local time today
def schedule_one_time_at(sched: AsyncIOScheduler, hour: int, minute: int):
    now = dt.datetime.now(TZ)
    run_at = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if run_at <= now:
        run_at = run_at + dt.timedelta(days=1)
    sched.add_job(refresh_all, "date", run_date=run_at, id=f"oneoff_{hour:02d}{minute:02d}")
    print(f"[scheduler] one-time refresh scheduled at {run_at}")

