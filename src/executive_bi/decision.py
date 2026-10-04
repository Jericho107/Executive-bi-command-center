from __future__ import annotations

from dataclasses import replace
from html import escape
from pathlib import Path

from .core import ExecutiveRecord, action_register, analyse, sample


def stress_records(
    records: list[ExecutiveRecord],
    revenue_shock_pct: float = -0.08,
    cash_shock_pct: float = -0.10,
    retention_shock_pct: float = -0.03,
) -> list[ExecutiveRecord]:
    if revenue_shock_pct > 0 or cash_shock_pct > 0 or retention_shock_pct > 0:
        raise ValueError("stress shocks must be non-positive")
    output: list[ExecutiveRecord] = []
    for row in records:
        retained = max(0, round(row.retained_customers * (1 + retention_shock_pct)))
        output.append(
            replace(
                row,
                revenue=row.revenue * (1 + revenue_shock_pct),
                gross_profit=row.gross_profit * (1 + revenue_shock_pct),
                cash_collected=row.cash_collected * (1 + cash_shock_pct),
                retained_customers=retained,
            )
        )
    return output


def scenario_comparison(records: list[ExecutiveRecord] | None = None) -> list[dict[str, object]]:
    base_records = records or sample()
    base_signals = {row.business_unit: row for row in analyse(base_records)}
    stress_signals = {row.business_unit: row for row in analyse(stress_records(base_records))}
    return [
        {
            "business_unit": unit,
            "base_priority": base_signals[unit].priority,
            "stress_priority": stress_signals[unit].priority,
            "base_driver_count": base_signals[unit].adverse_driver_count,
            "stress_driver_count": stress_signals[unit].adverse_driver_count,
            "priority_deteriorated": (
                stress_signals[unit].adverse_driver_count
                > base_signals[unit].adverse_driver_count
            ),
        }
        for unit in sorted(base_signals)
    ]


def executive_report_html() -> str:
    signals = analyse(sample())
    actions = action_register(signals)
    scenario = scenario_comparison()
    signal_rows = "".join(
        "<tr>"
        f"<td>{escape(row.business_unit)}</td>"
        f"<td>{row.revenue_variance_pct:.1%}</td>"
        f"<td>{row.gross_margin_pct:.1%}</td>"
        f"<td>{row.cash_conversion_pct:.1%}</td>"
        f"<td>{row.retention_pct:.1%}</td>"
        f"<td>{escape(row.priority)}</td>"
        "</tr>"
        for row in signals
    )
    action_rows = "".join(
        "<tr>"
        f"<td>{escape(str(row['business_unit']))}</td>"
        f"<td>{escape(str(row['priority']))}</td>"
        f"<td>{escape(', '.join(row['drivers']))}</td>"
        f"<td>{escape(str(row['owner']))}</td>"
        f"<td>{escape(str(row['follow_up_metric']))}</td>"
        "</tr>"
        for row in actions
    )
    stress_rows = "".join(
        "<tr>"
        f"<td>{escape(str(row['business_unit']))}</td>"
        f"<td>{escape(str(row['base_priority']))}</td>"
        f"<td>{escape(str(row['stress_priority']))}</td>"
        f"<td>{row['base_driver_count']}</td>"
        f"<td>{row['stress_driver_count']}</td>"
        "</tr>"
        for row in scenario
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><title>Executive BI Command Center</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 1180px; margin: 40px auto; line-height: 1.45; }}
table {{ border-collapse: collapse; width: 100%; margin: 1rem 0 2rem; }}
th, td {{ border: 1px solid #ddd; padding: .55rem; text-align: right; }}
th:first-child, td:first-child {{ text-align: left; }}
</style>
</head>
<body>
<h1>Executive BI Command Center</h1>
<p>Cross-functional decision surface for revenue, margin, cash conversion and retention.</p>
<h2>Current operating signals</h2>
<table><thead><tr><th>Unit</th><th>Revenue variance</th><th>Gross margin</th><th>Cash conversion</th><th>Retention</th><th>Priority</th></tr></thead><tbody>{signal_rows}</tbody></table>
<h2>Action register</h2>
<table><thead><tr><th>Unit</th><th>Priority</th><th>Drivers</th><th>Owner</th><th>Follow-up metric</th></tr></thead><tbody>{action_rows}</tbody></table>
<h2>Downside stress test</h2>
<table><thead><tr><th>Unit</th><th>Base priority</th><th>Stress priority</th><th>Base drivers</th><th>Stress drivers</th></tr></thead><tbody>{stress_rows}</tbody></table>
<p><small>Synthetic management data. Thresholds require calibration before operational deployment.</small></p>
</body></html>"""


def write_executive_report(path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(executive_report_html(), encoding="utf-8")
    return output
