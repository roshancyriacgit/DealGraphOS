
from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class DealSubstrate:
    id: str
    name: str
    jurisdiction: str
    status: str
    assumptions: Dict[str, Any] = field(default_factory=dict)
    parties: List[Dict[str, Any]] = field(default_factory=list)
    instruments: List[Dict[str, Any]] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    checklist_items: List[Dict[str, Any]] = field(default_factory=list)
    documents: List[Dict[str, Any]] = field(default_factory=list)
    risk_flags: List[Dict[str, Any]] = field(default_factory=list)
