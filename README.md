<div align="center">

# Executive BI Command Center

### Cross-functional executive decision system for revenue, margin, cash conversion and retention.

**Pretoria BI — Data · Intelligence · Performance**

</div>

---

## Management question

> Revenue can be on plan while margin, cash conversion or retention deteriorate. **Which unit requires management attention first, and why?**

**All data and entities are synthetic. No client result or realised ROI is claimed.**

---

## What this repository proves

- Revenue vs budget variance
- Gross margin and controllable contribution
- Cash conversion
- Retention
- Driver-count based action priority

The objective is not to inflate a portfolio with screenshots. The repository has an executable happy path and deliberately corrupted states that must be rejected.

## Evidence chain

```text
SIGNAL → CONTRACT → VALIDATION → ANALYSIS → DECISION RULE → ACTION OWNER → FOLLOW-UP
```

## Run locally

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -q
python -m executive_bi.cli smoke
python -m executive_bi.cli reverse-test
```

## Repository map

```text
executive-bi-command-center/
├── .github/workflows/ci.yml
├── config/
├── docs/
├── sql/
├── src/executive_bi/
├── tests/
├── Dockerfile
├── Makefile
├── pyproject.toml
└── README.md
```

## Proof boundary

Implemented evidence is separated from future production claims. See `docs/proof_matrix.md` and `docs/limitations.md`. Thresholds in this synthetic case are examples to demonstrate governance and must be calibrated before real deployment.

---

<div align="center">

**Pretoria BI**  
**Understand · Decide · Act · Measure**

</div>
