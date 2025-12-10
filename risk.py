
from typing import Optional
from sqlmodel import SQLModel, Field

class RiskFlag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deal.id")
    code: str
    severity: str  # red / amber / green
    title: str
    description: str
    rule_ids: Optional[str] = None       # JSON list as string
    assumptions: Optional[str] = None    # JSON dict as string
