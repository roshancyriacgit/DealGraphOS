
from typing import Optional
from sqlmodel import SQLModel, Field

class ChecklistItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deal.id")
    label: str
    status: str = "pending"  # pending / in_progress / done
    owner_role: str = "A0"   # A0 / associate / partner / client etc.
    dependencies: Optional[str] = None  # JSON list of ids as string for now
