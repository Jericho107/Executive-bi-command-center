# Validation Matrix

| Claim | Executable evidence | Failure path | Status |
|---|---|---|---|
| Unit/period grain is unique | `core.validate` | duplicate period/business unit | implemented |
| Financial relationships remain plausible | `core.validate` | impossible margin/cash/cost state | implemented |
| KPI signals are deterministic | `core.analyse` | boundary tests | implemented |
| Priority is tied to adverse business drivers | adverse-driver count + priority rules | controlled stress scenario | implemented |
| Every actionable signal has an owner and follow-up metric | `action_register` | action-register tests | implemented |
| Decision layer responds to downside conditions | `decision.stress_records` + comparison | stress responsiveness reverse test | implemented |
| Executive report is generated from the governed model | `decision.executive_report_html` | report-content tests | implemented |
| CI validates clean and corrupted states | GitHub Actions | duplicate/impossible state + stress reverse tests | implemented |
| Real management impact | no production evidence | not applicable | not claimed |

## Review principle

The project does not treat a KPI as an action. A signal must be connected to a driver, priority, owner and follow-up metric before it reaches the action register.
