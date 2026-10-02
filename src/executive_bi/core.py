from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass


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
    for row in records:
        key = (row.period, row.business_unit)
        if key in seen:
            raise ValueError(f"duplicate grain: {key}")
        seen.add(key)
        if not row.period or not row.business_unit:
            raise ValueError("period and business_unit are required")
        financials = [
            row.revenue,
            row.budget_revenue,
            row.gross_profit,
            row.controllable_cost,
            row.cash_collected,
            row.billed_revenue,
        ]
        if min(financials) < 0:
            raise ValueError("financial values must be non-negative")
        if row.gross_profit > row.revenue:
            raise ValueError("gross profit cannot exceed revenue")
        if row.controllable_cost > row.revenue * 2:
            raise ValueError("controllable cost outside plausibility bound")
        if row.cash_collected > row.billed_revenue * 1.25:
            raise ValueError("cash collection outside plausibility bound")
        if not 0 <= row.retained_customers <= row.opening_customers:
            raise ValueError("retention counts are inconsistent")


def analyse(records: Iterable[ExecutiveRecord]) -> list[ExecutiveSignal]:
    rows = list(records)
    validate(rows)
    output: list[ExecutiveSignal] = []
    for row in rows:
        variance = (
            (row.revenue - row.budget_revenue) / row.budget_revenue
            if row.budget_revenue
            else 0.0
        )
        margin = row.gross_profit / row.revenue if row.revenue else 0.0
        cash = row.cash_collected / row.billed_revenue if row.billed_revenue else 0.0
        retention = (
            row.retained_customers / row.opening_customers
            if row.opening_customers
            else 0.0
        )
        contribution = row.gross_profit - row.controllable_cost
        adverse = sum(
            (
                variance < -0.05,
                margin < 0.30,
                cash < 0.85,
                retention < 0.90,
                contribution < 0,
            )
        )
        priority = "high" if adverse >= 2 else "medium" if adverse == 1 else "monitor"
        output.append(
            ExecutiveSignal(
                row.period,
                row.business_unit,
                variance,
                margin,
                contribution,
                cash,
                retention,
                adverse,
                priority,
            )
        )
    return output


def action_register(signals: Iterable[ExecutiveSignal]) -> list[dict[str, object]]:
    actions: list[dict[str, object]] = []
    for row in signals:
        if row.priority == "monitor":
            continue
        drivers: list[str] = []
        if row.revenue_variance_pct < -0.05:
            drivers.append("revenue_variance")
        if row.gross_margin_pct < 0.30:
            drivers.append("gross_margin")
        if row.cash_conversion_pct < 0.85:
            drivers.append("cash_conversion")
        if row.retention_pct < 0.90:
            drivers.append("retention")
        if row.controllable_contribution < 0:
            drivers.append("controllable_contribution")
        actions.append(
            {
                "period": row.period,
                "business_unit": row.business_unit,
                "priority": row.priority,
                "drivers": drivers,
                "owner": "business_unit_lead",
                "follow_up_metric": drivers[0] if drivers else "priority",
            }
        )
    return actions


def portfolio_summary(signals: Iterable[ExecutiveSignal]) -> dict[str, object]:
    rows = list(signals)
    return {
        "units": len(rows),
        "high_priority_units": [
            row.business_unit for row in rows if row.priority == "high"
        ],
        "total_controllable_contribution": round(
            sum(row.controllable_contribution for row in rows),
            2,
        ),
    }


def sample() -> list[ExecutiveRecord]:
    return [
        ExecutiveRecord(
            "2026-09", "North", 980000, 1000000, 360000, 220000,
            875000, 990000, 910, 1000,
        ),
        ExecutiveRecord(
            "2026-09", "South", 760000, 850000, 205000, 230000,
            610000, 790000, 830, 950,
        ),
        ExecutiveRecord(
            "2026-09", "Digital", 520000, 500000, 190000, 105000,
            505000, 520000, 965, 1000,
        ),
    ]


def serialise_sample() -> dict[str, object]:
    signals = analyse(sample())
    return {
        "signals": [asdict(item) for item in signals],
        "actions": action_register(signals),
        "summary": portfolio_summary(signals),
    }
