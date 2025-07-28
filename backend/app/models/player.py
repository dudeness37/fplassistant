from sqlmodel import SQLModel, Field
from typing import Optional

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fpl_element_id: int = Field(index=True, unique=True)
    first_name: str
    second_name: str
    web_name: str
    team_id: int = Field(index=True)  # FPL team id
    element_type: int  # 1=GK,2=DEF,3=MID,4=FWD
    now_cost: int  # tenths
    status: str
    minutes_prev: int | None = None
    goals_prev: int | None = None
    assists_prev: int | None = None
