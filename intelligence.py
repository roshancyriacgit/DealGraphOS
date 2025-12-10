
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from ..models.db import get_session
from ..models.deal import Deal
from ..core.substrate import DealSubstrate
from ..core.rules_engine import RulesEngine
from pathlib import Path

router = APIRouter()

RULES_BASE_DIR = Path(__file__).resolve().parent.parent / "rules" / "jurisdictions" / "india"

class IntelligenceResponseItem(Dict[str, Any]):
    pass

@router.get("/{deal_id}")
def compute_intelligence(deal_id: int) -> Dict[str, List[Dict[str, Any]]]:
    """
    Compute high-level Indian corporate / regulatory workflow and risk signals
    for a given deal, based on YAML rule packs.
    """
    with get_session() as session:
        deal = session.get(Deal, deal_id)
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")

        substrate = DealSubstrate(
            id=str(deal.id),
            name=deal.name,
            jurisdiction=deal.jurisdiction,
            status=deal.status,
        )

        context = {
            "jurisdiction": deal.jurisdiction,
            "listed": deal.listed,
            "has_non_resident_investor": deal.has_non_resident_investor,
            "deal_size_crore": deal.deal_size_crore,
            "sector": deal.sector,
            "control_acquisition_percent": deal.control_acquisition_percent,
        }

        engine = RulesEngine.load_from_dir(RULES_BASE_DIR)
        result = engine.evaluate(substrate, context=context)

        return {
            "checklist": result.new_checklist_items,
            "risks": result.new_risk_flags,
        }
