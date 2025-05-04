from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password_hash: str
    xp: int = 0
    badge: Optional[str] = None   # “Bronz”, “Gümüş”, “Altın”