<div align="center">

# Executive BI Command Center

### Revenue · Margin · Cash Conversion · Retention · Action Priority

**Python · Decision Rules · Scenario Analysis · CI**

**Pretoria BI — Data · Intelligence · Performance**

</div>

---

## Management question

> **Which business unit requires management attention first, why, who owns the response and what happens under a downside scenario?**

This repository turns cross-functional management metrics into an explicit action register rather than stopping at KPI display.

**All entities and values are synthetic. No client result or realised ROI is claimed.**

## Decision model

```text
ACTUALS + BUDGET + CASH + CUSTOMER BASE
                 ↓
           DATA CONTRACTS
                 ↓
       GOVERNED KPI CALCULATION
                 ↓
       ADVERSE DRIVER DETECTION
                 ↓
         PRIORITY CLASSIFICATION
                 ↓
OWNER + FOLLOW-UP METRIC + STRESS TEST
```

Implemented signals:

- revenue vs budget variance;
- gross margin;
- controllable contribution;
- cash conversion;
- customer retention;
- adverse-driver count;
- unit-level action priority.

## Executive decision surface

Generate the management report:

```bash
python -m executive_bi.cli report
```

Output: `output/executive_command_center.html`.

The report contains the current unit ranking, action register and a downside scenario that shocks revenue, cash collection and retention.

## Stress-test discipline

A model that never changes when operating conditions deteriorate is not useful for management. The repository therefore verifies that a controlled downside scenario increases or preserves adverse-driver pressure and changes priority where appropriate.

## Run locally

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -q
python -m executive_bi.cli smoke
python -m executive_bi.cli report
python -m executive_bi.cli reverse-test
```

## Review path

**For a recruiter:** inspect `core.py`, `decision.py`, tests and CI.  
**For a manager:** open the generated HTML report and read the action register.

Thresholds are demonstrative and require calibration against the economics and risk appetite of a real organisation.

---

<div align="center">

**Pretoria BI**  
**Understand · Decide · Act · Measure**

</div>
