
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Party(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deal.id")
    name: str
    role: str  # acquirer / target / investor / promoter / lender etc.
    residency: str = "resident"
    listed: bool = False
    group_tag: Optional[str] = None
