from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class ExecutiveRecord:
    period: str
    business_unit: str
    revenue: float
    budget_revenue: float
    gross_profit: float
    controllable_cost: float
    cash_collected: float
    billed_revenue: float
    retained_customers: int
    opening_customers: int


@dataclass(frozen=True)
class ExecutiveSignal:
    period: str
    business_unit: str
    revenue_variance_pct: float
    gross_margin_pct: float
    controllable_contribution: float
    cash_conversion_pct: float
    retention_pct: float
    adverse_driver_count: int
    priority: str


def validate(records: Iterable[ExecutiveRecord]) -> None:
    seen: set[tuple[str, str]] = set()
    for r in records:
        key = (r.period, r.business_unit)
        if key in seen:
            raise ValueError(f"duplicate grain: {key}")
        seen.add(key)
        if not r.period or not r.business_unit:
            raise ValueError("period and business_unit are required")
        financials = [r.revenue, r.budget_revenue, r.gross_profit, r.controllable_cost,
                      r.cash_collected, r.billed_revenue]
        if min(financials) < 0:
            raise ValueError("financial values must be non-negative")
        if r.gross_profit > r.revenue:
            raise ValueError("gross profit cannot exceed revenue")
        if r.controllable_cost > r.revenue * 2:
            raise ValueError("controllable cost outside plausibility bound")
        if r.cash_collected > r.billed_revenue * 1.25:
            raise ValueError("cash collection outside plausibility bound")
        if not 0 <= r.retained_customers <= r.opening_customers:
            raise ValueError("retention counts are inconsistent")


def analyse(records: Iterable[ExecutiveRecord]) -> list[ExecutiveSignal]:
    rows = list(records)
    validate(rows)
    out: list[ExecutiveSignal] = []
    for r in rows:
        variance = (r.revenue - r.budget_revenue) / r.budget_revenue if r.budget_revenue else 0.0
        margin = r.gross_profit / r.revenue if r.revenue else 0.0
        cash = r.cash_collected / r.billed_revenue if r.billed_revenue else 0.0
        retention = r.retained_customers / r.opening_customers if r.opening_customers else 0.0
        contribution = r.gross_profit - r.controllable_cost
        adverse = sum((variance < -0.05, margin < 0.30, cash < 0.85, retention < 0.90, contribution < 0))
        priority = "high" if adverse >= 2 else "medium" if adverse == 1 else "monitor"
        out.append(ExecutiveSignal(r.period, r.business_unit, variance, margin, contribution,
                                   cash, retention, adverse, priority))
    return out


def portfolio_summary(signals: Iterable[ExecutiveSignal]) -> dict[str, object]:
    rows = list(signals)
    return {
        "units": len(rows),
        "high_priority_units": [r.business_unit for r in rows if r.priority == "high"],
        "total_controllable_contribution": round(sum(r.controllable_contribution for r in rows), 2),
    }


def sample() -> list[ExecutiveRecord]:
    return [
        ExecutiveRecord("2026-09", "North", 980000, 1000000, 360000, 220000, 875000, 990000, 910, 1000),
        ExecutiveRecord("2026-09", "South", 760000, 850000, 205000, 230000, 610000, 790000, 830, 950),
        ExecutiveRecord("2026-09", "Digital", 520000, 500000, 190000, 105000, 505000, 520000, 965, 1000),
    ]


def serialise_sample() -> dict[str, object]:
    signals = analyse(sample())
    return {"signals": [asdict(x) for x in signals], "summary": portfolio_summary(signals)}
