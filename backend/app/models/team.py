from sqlmodel import SQLModel, Field
from typing import Optional

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fpl_team_id: int = Field(index=True, unique=True)
    name: str
    short_name: str
    strength: int | None = None
    strength_attack_home: int | None = None
    strength_attack_away: int | None = None
    strength_defence_home: int | None = None
    strength_defence_away: int | None = None
