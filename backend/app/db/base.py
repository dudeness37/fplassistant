from sqlmodel import SQLModel
# Import models here so they are registered with SQLModel.metadata
from app.models.user import User  # noqa: F401

# You could add more models imports as they are created.
