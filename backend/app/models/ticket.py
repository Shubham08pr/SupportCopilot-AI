from pydantic import BaseModel
from typing import Optional


class Ticket(BaseModel):
    id: int
    query: str
    status: str = "open"
    ai_response: Optional[str] = None