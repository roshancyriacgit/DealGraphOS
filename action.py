
from typing import Optional
from sqlmodel import SQLModel, Field

class Action(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deal.id")
    category: str  # approval / filing / cp / closing_step / diligence etc.
    name: str
    description: Optional[str] = None
    sequence_hint: Optional[int] = None
    deadline_relative: Optional[int] = None  # days relative to signing/closing etc.
