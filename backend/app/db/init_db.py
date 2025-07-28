from sqlmodel import SQLModel
from app.db.session import engine

from app.models.user import User  # noqa
from app.models.team import Team  # noqa
from app.models.player import Player  # noqa
from app.models.fixture import Fixture  # noqa
from app.models.ep import EPRecord  # noqa

def init_db():
    SQLModel.metadata.create_all(bind=engine)
