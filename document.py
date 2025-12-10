
from typing import Optional
from sqlmodel import SQLModel, Field

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deal.id")
    template_key: str  # term_sheet / spa / ssa / resolutions etc.
    path: Optional[str] = None
    status: str = "drafted"  # drafted / reviewed / sent
