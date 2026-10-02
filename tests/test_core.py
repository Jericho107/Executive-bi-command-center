import pytest

from executive_bi.core import ExecutiveRecord, action_register, analyse, sample, validate


def test_high_priority_unit_is_exposed() -> None:
    signals = analyse(sample())
    south = next(item for item in signals if item.business_unit == "South")
    assert south.priority == "high"
    assert south.controllable_contribution < 0


def test_duplicate_grain_fails() -> None:
    rows = sample()
    with pytest.raises(ValueError, match="duplicate grain"):
        validate(rows + [rows[0]])


def test_impossible_margin_fails() -> None:
    with pytest.raises(ValueError, match="gross profit"):
        validate(
            [
                ExecutiveRecord(
                    "2026-09",
                    "X",
                    100,
                    100,
                    101,
                    20,
                    80,
                    100,
                    90,
                    100,
                )
            ]
        )


def test_high_priority_signal_has_action_owner_and_driver() -> None:
    actions = action_register(analyse(sample()))
    south = next(row for row in actions if row["business_unit"] == "South")
    assert south["owner"] == "business_unit_lead"
    assert "revenue_variance" in south["drivers"]
    assert south["follow_up_metric"]
