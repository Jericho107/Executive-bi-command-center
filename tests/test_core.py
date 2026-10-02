from executive_bi.core import ExecutiveRecord, analyse, sample, validate
import pytest

def test_high_priority_unit_is_exposed():
    signals = analyse(sample())
    south = next(x for x in signals if x.business_unit == "South")
    assert south.priority == "high"
    assert south.controllable_contribution < 0

def test_duplicate_grain_fails():
    rows = sample()
    with pytest.raises(ValueError, match="duplicate grain"):
        validate(rows + [rows[0]])

def test_impossible_margin_fails():
    with pytest.raises(ValueError, match="gross profit"):
        validate([ExecutiveRecord("2026-09","X",100,100,101,20,80,100,90,100)])
