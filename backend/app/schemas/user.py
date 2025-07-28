from pydantic import BaseModel

class UserCreate(BaseModel):
    telegram_chat_id: str
