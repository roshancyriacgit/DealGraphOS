
from typing import Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal

class Instrument(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deal.id")
    type: str  # equity / ccd / ncd / option / guarantee etc.
    issuer_party_id: Optional[int] = Field(default=None, foreign_key="party.id")
    holder_party_id: Optional[int] = Field(default=None, foreign_key="party.id")
    percentage: Optional[float] = None
    amount: Optional[Decimal] = None
    terms: Optional[str] = None  # JSON or text blob for now
