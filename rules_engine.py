
from dataclasses import dataclass, field
from typing import Any, Dict, List
from pathlib import Path

import yaml

from .substrate import DealSubstrate

@dataclass
class RuleResult:
    new_actions: List[Dict[str, Any]] = field(default_factory=list)
    new_checklist_items: List[Dict[str, Any]] = field(default_factory=list)
    new_risk_flags: List[Dict[str, Any]] = field(default_factory=list)
    updated_assumptions: Dict[str, Any] = field(default_factory=dict)

class RulesEngine:
    """
    Simple YAML-driven rule engine for deal-level Indian corporate / regulatory checks.

    Rule format (YAML):
      - id: "IN.CA.BOARD.001"
        name: "Board approvals under Companies Act"
        description: "Baseline board approvals for Indian corporate actions."
        scope: "companies_act"
        conditions:
          - field: "jurisdiction"
            op: "eq"
            value: "india"
        effects:
          checklist:
            - label: "Identify and obtain board approvals required under Companies Act (sections, rules, AoA)."
              owner_role: "associate"
          risks: []
    """

    def __init__(self, rules: List[Dict[str, Any]] | None = None):
        self.rules = rules or []

    @staticmethod
    def load_from_dir(rules_dir: Path) -> "RulesEngine":
        collected: List[Dict[str, Any]] = []
        if rules_dir.exists():
            for path in rules_dir.rglob("*.yml"):
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
                if isinstance(data, list):
                    collected.extend(data)
        return RulesEngine(collected)

    @staticmethod
    def _condition_passes(cond: Dict[str, Any], ctx: Dict[str, Any]) -> bool:
        field = cond.get("field")
        op = cond.get("op", "eq")
        value = cond.get("value")
        actual = ctx.get(field)
        if op == "eq":
            return (actual is not None) and (str(actual).lower() == str(value).lower())
        if op == "ne":
            return (actual is None) or (str(actual).lower() != str(value).lower())
        if op == "gte":
            try:
                return actual is not None and float(actual) >= float(value)
            except Exception:
                return False
        if op == "gt":
            try:
                return actual is not None and float(actual) > float(value)
            except Exception:
                return False
        if op == "lte":
            try:
                return actual is not None and float(actual) <= float(value)
            except Exception:
                return False
        if op == "lt":
            try:
                return actual is not None and float(actual) < float(value)
            except Exception:
                return False
        if op == "is_true":
            return bool(actual)
        if op == "is_false":
            return not bool(actual)
        if op == "in":
            if isinstance(value, list):
                return actual in value
            return False
        return False

    def evaluate(self, substrate: DealSubstrate, context: Dict[str, Any] | None = None) -> RuleResult:
        ctx = {
            "deal_id": substrate.id,
            "name": substrate.name,
            "jurisdiction": substrate.jurisdiction,
        }
        # merge extra context (e.g. deal fields) if provided
        if context:
            ctx.update(context)

        result = RuleResult()
        for rule in self.rules:
            conditions = rule.get("conditions", [])
            if conditions:
                if not all(self._condition_passes(c, ctx) for c in conditions):
                    continue

            effects = rule.get("effects", {})
            for c in effects.get("checklist", []):
                result.new_checklist_items.append(
                    {
                        "label": c.get("label", ""),
                        "owner_role": c.get("owner_role", "associate"),
                        "source_rule_id": rule.get("id"),
                        "scope": rule.get("scope"),
                    }
                )
            for r in effects.get("risks", []):
                result.new_risk_flags.append(
                    {
                        "code": r.get("code"),
                        "severity": r.get("severity", "amber"),
                        "title": r.get("title"),
                        "description": r.get("description"),
                        "source_rule_id": rule.get("id"),
                        "scope": rule.get("scope"),
                    }
                )
        return result
