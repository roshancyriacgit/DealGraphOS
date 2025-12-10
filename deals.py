
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..models.db import get_session
from ..models.deal import Deal

router = APIRouter()

class DealCreate(BaseModel):
    name: str
    jurisdiction: str = "india"
    description: str | None = None
    listed: bool = False
    has_non_resident_investor: bool = False
    deal_size_crore: float | None = None
    sector: str | None = None
    control_acquisition_percent: float | None = None

class DealRead(BaseModel):
    id: int
    name: str
    jurisdiction: str
    description: str | None
    status: str
    listed: bool
    has_non_resident_investor: bool
    deal_size_crore: float | None
    sector: str | None
    control_acquisition_percent: float | None

    class Config:
        orm_mode = True

@router.get("/", response_model=List[DealRead])
def list_deals():
    with get_session() as session:
        deals = session.query(Deal).order_by(Deal.created_at.desc()).all()
        return deals

@router.post("/", response_model=DealRead)
def create_deal(payload: DealCreate):
    with get_session() as session:
        deal = Deal(
            name=payload.name,
            jurisdiction=payload.jurisdiction,
            description=payload.description,
            listed=payload.listed,
            has_non_resident_investor=payload.has_non_resident_investor,
            deal_size_crore=payload.deal_size_crore,
            sector=payload.sector,
            control_acquisition_percent=payload.control_acquisition_percent,
        )
        session.add(deal)
        session.commit()
        session.refresh(deal)
        return deal

@router.get("/{deal_id}", response_model=DealRead)
def get_deal(deal_id: int):
    with get_session() as session:
        deal = session.get(Deal, deal_id)
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        return deal
