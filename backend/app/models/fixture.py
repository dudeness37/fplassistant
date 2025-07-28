from sqlmodel import SQLModel, Field
from typing import Optional

class Fixture(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fpl_fixture_id: int = Field(index=True, unique=True)
    event: int | None = Field(index=True)  # GW
    team_h: int
    team_a: int
    finished: bool | None = False
