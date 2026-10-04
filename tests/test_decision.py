import pytest

from executive_bi.core import sample
from executive_bi.decision import executive_report_html, scenario_comparison, stress_records


def test_stress_scenario_increases_or_preserves_driver_pressure():
    comparison = scenario_comparison()
    assert any(row["priority_deteriorated"] for row in comparison)
    assert all(row["stress_driver_count"] >= row["base_driver_count"] for row in comparison)


def test_positive_shock_is_rejected():
    with pytest.raises(ValueError, match="non-positive"):
        stress_records(sample(), revenue_shock_pct=0.05)


def test_report_contains_actions_and_stress_test():
    html = executive_report_html()
    assert "Action register" in html
    assert "Downside stress test" in html
    assert "South" in html
    assert "business_unit_lead" in html
