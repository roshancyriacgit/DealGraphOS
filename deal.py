
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field

class Deal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    jurisdiction: str = "india"
    description: Optional[str] = None
    status: str = "intake"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Indian corporate deal context (extensible)
    listed: bool = False
    has_non_resident_investor: bool = False
    deal_size_crore: Optional[float] = None
    sector: Optional[str] = None
    control_acquisition_percent: Optional[float] = None
