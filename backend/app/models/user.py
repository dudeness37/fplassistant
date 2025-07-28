from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_chat_id: Optional[str] = Field(default=None, index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
