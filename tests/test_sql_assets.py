import sqlite3
from pathlib import Path

import pytest

from executive_bi.core import analyse, sample

ROOT = Path(__file__).resolve().parents[1]


def _sql(name: str) -> str:
    return (ROOT / "sql" / name).read_text(encoding="utf-8")


def _database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.executescript(_sql("00_executive_schema.sql"))
    connection.executemany(
        """
        INSERT INTO fact_executive_period VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                row.period,
                row.business_unit,
                row.revenue,
                row.budget_revenue,
                row.gross_profit,
                row.controllable_cost,
                row.cash_collected,
                row.billed_revenue,
                row.retained_customers,
                row.opening_customers,
            )
            for row in sample()
        ],
    )
    return connection


def test_sql_kpis_reconcile_with_python_signals():
    python = {row.business_unit: row for row in analyse(sample())}
    connection = _database()
    rows = connection.execute(_sql("10_executive_kpis.sql")).fetchall()

    for row in rows:
        unit = row[1]
        assert row[2] == pytest.approx(python[unit].revenue_variance_pct)
        assert row[3] == pytest.approx(python[unit].gross_margin_pct)
        assert row[4] == pytest.approx(python[unit].controllable_contribution)
        assert row[5] == pytest.approx(python[unit].cash_conversion_pct)
        assert row[6] == pytest.approx(python[unit].retention_pct)


def test_sql_priority_reconciles_with_python_priority():
    python = {row.business_unit: row for row in analyse(sample())}
    connection = _database()
    rows = connection.execute(_sql("20_priority_ranking.sql")).fetchall()

    for row in rows:
        unit = row[1]
        assert row[7] == python[unit].adverse_driver_count
        assert row[8] == python[unit].priority
