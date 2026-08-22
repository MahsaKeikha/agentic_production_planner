# F112 | Agentic Production Planner | L3 Gold Standard | v1.0

A governed multi-agent reference system for production planning support, including demand review, capacity analysis, scheduling, materials planning, inventory assumptions, constraint review, and qualified human approval.

## Five-agent architecture

- Demand Agent
- Capacity Agent
- Scheduling Agent
- Materials Agent
- Reviewer Agent

## Gold-standard production governance

F112 is fail closed and planning support only. Release requires reviewed demand, capacity, materials, schedule, inventory, quality and safety dependencies, change control, and explicit qualified-human approval.

Release is blocked for unbounded demand uncertainty, capacity overload, unresolved material shortages, lead-time conflicts, inventory inaccuracies, infeasible schedules, quality or safety holds, unreviewed material planning changes, or traceability gaps.

The reference system cannot autonomously release production schedules, override constraints, commit inventory, authorize production, make supplier commitments, or override quality or safety holds. Final production decisions remain with authorized planners, operations leaders, quality, and safety personnel.

## Verification gates

CI runs on Python 3.10, 3.11, and 3.12 and requires:

```bash
ruff check . --select E9,F63,F7,F82
python -m pytest -q
python evals/held_out.py
python run.py
```

The behavioral verification layer includes eight direct governance tests and a 10-scenario held-out production-planning suite.
