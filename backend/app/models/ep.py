from sqlmodel import SQLModel, Field
from typing import Optional

class EPRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    gw: int = Field(index=True)
    fpl_element_id: int = Field(index=True)
    ep: float
    variance: float | None = None
