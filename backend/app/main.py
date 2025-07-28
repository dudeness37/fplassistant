from fastapi import FastAPI
from app.core.logging import logger
from app.db.init_db import init_db
from app.routers import health, telegram, admin, players, fixtures, ep, optimize
from app.services.scheduler import start_scheduler

app = FastAPI(title="FPL AI Backend", version="0.2.0")

@app.on_event("startup")
def on_startup():
    logger.info("Starting up...")
    init_db()
    start_scheduler()

app.include_router(health.router, prefix="/api")
app.include_router(telegram.router, prefix="/api")
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(players.router, prefix="/api", tags=["players"])
app.include_router(fixtures.router, prefix="/api", tags=["fixtures"])
app.include_router(ep.router, prefix="/api", tags=["ep"])
app.include_router(optimize.router, prefix="/api", tags=["optimize"])
