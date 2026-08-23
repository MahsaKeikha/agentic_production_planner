# F112 | Agentic Production Planner | L3 Gold Standard | v1.0

A governed five-agent reference architecture for production-planning support across demand review, capacity analysis, materials planning, inventory validation, constraint management, finite scheduling, quality and safety dependencies, change control, evidence traceability, and qualified human approval.

F112 is planning-support only. It creates reviewable production recommendations without exercising binding authority over production schedules, inventory commitments, supplier commitments, constraint overrides, production authorization, or quality and safety holds.

## Production planning lifecycle

```text
Demand and Order Context
        -> Capacity Review
        -> Materials and Inventory Review
        -> Constraint Analysis
        -> Schedule Construction
        -> Quality and Safety Dependency Review
        -> Change-Control Review
        -> Qualified Human Approval
```

The workflow is fail closed. Unbounded demand uncertainty, overloaded capacity, material shortages, lead-time conflicts, inaccurate inventory, infeasible schedules, quality or safety holds, unreviewed plan changes, traceability gaps, or missing required reviews prevent release.

## Five-agent architecture

| Agent | Responsibility | Core question |
|---|---|---|
| Demand Agent | Reviews demand signals, orders, forecasts, priorities, uncertainty, and planning assumptions | What demand should the plan actually represent, and how uncertain is it? |
| Capacity Agent | Reviews available capacity, calendars, bottlenecks, utilization, and load | Can the required work fit within reviewed capacity? |
| Scheduling Agent | Builds and evaluates feasible production sequences under known constraints | Is the proposed schedule executable without hidden conflicts? |
| Materials Agent | Reviews material availability, lead times, inventory assumptions, shortages, and dependencies | Are required materials actually available when needed? |
| Reviewer Agent | Performs independent readiness and governance review | Is the recommendation package sufficiently reviewed for authorized human action? |

The agents support planners and operations personnel. They do not replace production control, quality, safety, procurement, supply-chain, engineering, maintenance, finance, or authorized operations leadership.

## Repository structure

```text
AGENTS/
├── demand_agent.py
├── capacity_agent.py
├── scheduling_agent.py
├── materials_agent.py
└── reviewer_agent.py

SKILLS/
├── demand_reasoning.py
├── capacity_reasoning.py
├── scheduling_reasoning.py
├── constraint_reasoning.py
└── human_review.py

TOOLS/
├── capacity_calculator.py
├── constraint_register.py
├── evidence_register.py
├── review_gate.py
└── schedule_table.py

orchestration/
memory/
observability/
evals/
benchmarks/
examples/
docs/
prompts/
config/
safety/
tests/
.github/workflows/ci.yml
run.py
pyproject.toml
README.md
```

The architecture separates planning reasoning from deterministic capacity calculations, constraint registration, evidence tracking, schedule representation, review gates, observability, and evaluation.

## Planning context

A governed production-planning record can include:

```text
planning_horizon
site
line_or_workcenter
product
order_or_demand_id
quantity
due_date
priority
forecast
firm_order
routing
cycle_time
setup_time
calendar
capacity
material_requirements
inventory
lead_times
quality_status
safety_status
constraints
revision
source
review_state
```

Missing facts should remain explicit. F112 must not invent orders, inventory, capacity, lead times, routing, supplier commitments, quality release, safety clearance, or production authorization.

## Demand review

`SKILLS/demand_reasoning.py` supports structured review of production demand.

Demand can include:

- firm customer orders
- internal replenishment
- forecasts
- service requirements
- engineering builds
- prototypes
- maintenance demand
- safety stock replenishment
- backlog

The system should distinguish committed demand from forecast demand and planning scenarios.

The reference policy requires `demand_reviewed`.

## Demand uncertainty

Forecasts and orders can change. Demand review should preserve uncertainty rather than representing every demand signal as equally certain.

Useful dimensions include:

- source
- confidence
- volatility
- horizon
- order status
- cancellation risk
- upside and downside scenarios
- historical error
- known promotions or events

`demand_uncertainty_unbounded` blocks release when uncertainty is material but has not been adequately bounded for the planning decision.

## Demand prioritization

Production priorities can arise from customer commitments, service levels, safety needs, regulatory requirements, contractual obligations, inventory policies, or authorized business decisions.

F112 can organize priorities but should not invent priority rules or silently favor one customer, product, or business unit without an attributable policy or authorized decision.

## Capacity review

`SKILLS/capacity_reasoning.py` and `TOOLS/capacity_calculator.py` support capacity analysis.

Capacity review can consider:

- available hours
- shift calendars
- planned downtime
- changeovers
- staffing assumptions
- equipment availability
- tooling availability
- maintenance windows
- yield assumptions
- efficiency assumptions
- bottlenecks
- parallel resources

The reference policy requires `capacity_reviewed`.

## Capacity versus load

A production plan should distinguish theoretical, demonstrated, and available capacity.

Useful states include:

```text
nameplate capacity
historical demonstrated capacity
scheduled available capacity
committed load
planned load
remaining capacity
```

`capacity_overload` blocks release when planned load exceeds reviewed capacity.

The system should not solve an overload by silently assuming overtime, extra shifts, faster cycle time, skipped maintenance, reduced inspection, or additional labor.

## Bottleneck management

A bottleneck can move as product mix, staffing, downtime, setup, material availability, or routing changes.

F112 can identify bottleneck candidates and schedule implications. It should not treat a single historical bottleneck as permanently fixed without current evidence.

## Materials planning

The Materials Agent reviews whether required components, raw materials, consumables, packaging, subassemblies, and externally supplied items are available when needed.

Review can consider:

- bill of materials
- material requirements
- on-hand inventory
- allocated inventory
- open purchase orders
- transfer orders
- work in process
- safety stock
- scrap assumptions
- lot sizes
- shelf life
- approved substitutions
- supplier lead time

The reference policy requires `materials_reviewed`.

## Material shortages

`material_shortage` is an explicit fail-closed blocker.

The system should distinguish among:

```text
on hand
available to promise
allocated
quarantined
expired
quality hold
in transit
planned receipt
unconfirmed supply
```

A planned or requested receipt should not be represented as available inventory without appropriate evidence.

## Inventory review

The policy requires `inventory_reviewed`.

Inventory review can include:

- quantity accuracy
- location
- lot or serial status
- revision
- expiration
- quarantine status
- allocation
- cycle-count confidence
- ownership
- work-in-process status

`inventory_inaccuracy` blocks release when inventory accuracy or availability is unresolved.

## Lead-time discipline

Lead times can include supplier lead time, transit, receiving, inspection, internal queue, processing, curing, testing, release, and transfer time.

`lead_time_conflict` blocks release when schedule assumptions conflict with reviewed lead times.

F112 should not compress a lead time simply to make a requested due date appear feasible.

## Constraint reasoning

`SKILLS/constraint_reasoning.py` and `TOOLS/constraint_register.py` support explicit constraint management.

Constraints can include:

- equipment
- tooling
- labor or skills
- material
- supplier
- quality hold
- safety hold
- maintenance
- utilities
- cleanroom or environmental conditions
- sequence rules
- curing or dwell times
- inspection capacity
- storage
- transportation
- regulatory restrictions

A constraint should be recorded with its source, owner, affected work, timing, and resolution state when possible.

## Constraint hierarchy

Some constraints are negotiable planning assumptions. Others are hard boundaries.

Quality, safety, regulatory, physical, and authorized engineering constraints should not be treated as ordinary optimization penalties that the scheduler can trade away.

`override_constraint` is therefore a protected action.

## Scheduling

`SKILLS/scheduling_reasoning.py` and `TOOLS/schedule_table.py` support production-schedule construction and review.

A schedule can include:

```text
job
operation
resource
start
finish
setup
quantity
material_status
constraint_status
priority
due_date
slack
revision
```

The policy requires `schedule_reviewed`.

## Schedule feasibility

A schedule is not feasible merely because rows fit on a timeline.

Feasibility can depend on:

- resource availability
- precedence
- routing
- setup
- labor skills
- material availability
- tooling
- maintenance
- inspection
- quality release
- safety constraints
- transport
- shift calendars

`schedule_infeasible` blocks release.

## Finite versus infinite scheduling

F112 should distinguish finite-capacity schedules from infinite-capacity planning views.

An infinite-capacity plan can be useful for demand visualization, but it should not be labeled executable when resource capacity has not been enforced.

## Sequence-dependent setup

Setup and changeover time can depend on production sequence.

The system can support grouping or sequencing recommendations, but optimization should not override contamination controls, validated cleaning, allergen controls, tooling requirements, product segregation, quality requirements, or other hard constraints.

## Due dates and lateness

A planner can analyze:

- due-date performance
- lateness
- earliness
- slack
- backlog
- critical orders
- recovery scenarios

F112 should expose infeasibility rather than manufacture an on-time plan by violating capacity, material, quality, or safety assumptions.

## Work in process

Work-in-process status can materially affect the schedule.

Useful WIP information includes:

- current operation
- completed quantity
- remaining quantity
- hold status
- lot or serial identity
- rework status
- inspection status
- next eligible operation

Stale WIP information should be surfaced as uncertainty.

## Quality dependencies

The reference policy requires `quality_safety_dependencies_reviewed`.

Quality dependencies can include:

- incoming inspection
- first-article approval
- in-process inspection
- test availability
- nonconformance disposition
- deviation approval
- lot release
- validation status
- calibration status
- document revision

`quality_safety_hold` blocks release when a quality or safety dependency prevents production.

## Safety dependencies

Production planning should respect worker, equipment, process, and facility safety constraints.

Examples include:

- lockout or maintenance status
- unsafe equipment condition
- staffing competency
- hazardous-material controls
- occupancy limits
- required supervision
- process safety restrictions
- emergency restrictions

F112 cannot override a safety hold to meet schedule performance.

## Maintenance dependencies

Planned and unplanned maintenance can affect available capacity.

A production recommendation should preserve maintenance windows and equipment-out-of-service status. It should not consume maintenance time as available production capacity without authorized review.

## Calibration and equipment status

Equipment used for production, inspection, or testing may require valid calibration or qualification.

F112 should not schedule work as production-ready when required equipment status is unresolved.

## Labor and skills

Capacity can depend on qualified labor, certifications, training, supervision, and shift coverage.

The system may model labor constraints but cannot autonomously change staffing, employment terms, overtime, certifications, or competency requirements.

## Overtime and additional shifts

Overtime or extra shifts can be scenario variables only when explicitly authorized as assumptions.

F112 should not silently use overtime to eliminate overload or lateness.

## Supplier dependencies

Supplier receipts can constrain production.

A planning package can distinguish:

```text
requested date
supplier-confirmed date
expected date
actual receipt
quality-released date
```

`expedite_supplier_commitment` is protected. The system cannot commit a supplier or organization to expedited supply.

## Supplier commitment boundary

F112 may draft an escalation or identify a required expedite, but it cannot autonomously place, modify, accelerate, or financially commit a purchase or supplier order.

Supplier commitments remain with authorized procurement and supply-chain personnel.

## Inventory commitment boundary

`commit_inventory` is protected.

The system can recommend allocation scenarios but cannot autonomously reserve or commit scarce inventory to a customer, product, site, or order where that action has binding operational or commercial effect.

## Production authorization boundary

`authorize_production` is protected.

A reviewed planning package is not authorization to manufacture. Production release remains subject to authorized operations, engineering, quality, safety, and other required controls.

## Schedule-release boundary

`release_schedule` is protected.

F112 can generate a proposed schedule, but it cannot autonomously release that schedule as binding shop-floor direction.

## Quality and safety hold boundary

`override_quality_or_safety_hold` is protected.

No optimization target, customer priority, due date, cost, utilization goal, or executive preference allows the reference system to bypass a quality or safety hold.

## Change control

The policy requires `change_control_reviewed`.

Production plans can change because of:

- demand changes
- shortages
- supplier changes
- capacity changes
- equipment downtime
- engineering changes
- quality events
- safety events
- staffing changes
- priority changes
- maintenance

`unreviewed_plan_change` blocks release when a material planning change lacks appropriate change-control review.

## Frozen, slushy, and flexible horizons

Organizations may define planning time fences such as frozen, slushy, and flexible horizons.

F112 can model these policies when supplied, but it should not invent time-fence rules or autonomously break a frozen schedule.

## Engineering-change dependencies

A production schedule must respect approved product, process, routing, BOM, and document revisions.

The system should not schedule against an obsolete revision merely because the material or routing is available.

## Traceability

`TOOLS/evidence_register.py` supports evidence traceability.

Useful planning provenance includes:

```text
input
source
version
timestamp
owner
assumption
calculation
constraint
reviewer
approval
```

`traceability_gap` blocks release when material planning inputs or decisions cannot be traced.

## Evidence discipline

A governed plan should distinguish among:

```text
verified order
forecast
inventory record
supplier commitment
planning assumption
calculated capacity
system inference
human override
approved decision
```

These states should not be collapsed into one generic planning fact.

## Scenario planning

F112 can compare scenarios such as:

- baseline
- demand upside or downside
- alternate sequence
- alternate line
- authorized overtime assumption
- supplier-delay scenario
- equipment-down scenario
- material substitution scenario pending approval

Scenario output must clearly identify assumptions and should not be mistaken for an approved production plan.

## Optimization boundaries

Production optimization can target throughput, lateness, utilization, changeovers, inventory, cost, or other objectives.

Optimization must remain subordinate to hard constraints and governance. A mathematically improved schedule is unacceptable if it depends on unavailable material, unsafe operation, skipped quality controls, unapproved changes, or fictional capacity.

## Plan stability and nervousness

Frequent schedule changes can create operational instability.

A planning system can track:

- number of reschedules
- jobs moved
- magnitude of date changes
- frozen-horizon violations
- material reallocation
- labor disruption

F112 can surface plan nervousness as a tradeoff for qualified planners.

## Service level and business priorities

Service-level targets and business priorities can influence scheduling, but they should be attributable to approved policy or authorized decisions.

The system should not infer strategic customer importance from revenue, company name, or other proxy unless such a rule is explicitly supplied and appropriate.

## Fairness and allocation

When scarce capacity or inventory affects multiple customers or business units, allocation can have contractual and commercial consequences.

F112 can present transparent scenarios and tradeoffs. Binding allocation decisions remain with authorized humans.

## Data freshness

Production planning is highly time-sensitive.

Important inputs can become stale quickly, including:

- inventory
- WIP
- equipment status
- supplier dates
- demand
- holds
- labor availability

Implementations should preserve timestamps and identify stale inputs rather than presenting an old plan as current.

## Required reviews

The implemented safety policy requires all eight conditions:

```text
demand_reviewed
capacity_reviewed
materials_reviewed
schedule_reviewed
inventory_reviewed
quality_safety_dependencies_reviewed
change_control_reviewed
human_approval
```

Missing any required review fails closed.

## Fail-closed governance

The implemented policy blocks release for:

- inadequately bounded demand uncertainty
- planned load exceeding reviewed capacity
- unresolved required-material shortages
- lead-time assumptions conflicting with the schedule
- unresolved inventory accuracy or availability
- infeasible production schedules
- blocking quality or safety dependencies
- material planning changes lacking change-control review
- untraceable planning inputs or decisions
- missing required reviews
- missing human approval

The system should expose infeasibility rather than hiding it behind an apparently complete schedule.

## Protected actions

The safety policy permanently protects:

```text
release_schedule
override_constraint
commit_inventory
authorize_production
expedite_supplier_commitment
override_quality_or_safety_hold
```

These actions remain outside autonomous authority even when all review flags are satisfied.

## Human authority boundaries

F112 must not autonomously:

- release a production schedule
- authorize manufacturing
- override a production constraint
- override quality or safety holds
- commit scarce inventory
- commit or expedite a supplier
- change staffing or overtime
- approve engineering substitutions
- waive inspection or validation
- alter maintenance requirements
- represent a planning scenario as an approved operational decision

Final authority remains with qualified planners and the appropriate operations, engineering, quality, safety, procurement, supply-chain, maintenance, and business personnel.

## Independent human review

`SKILLS/human_review.py` and `TOOLS/review_gate.py` support explicit review before recommendation release.

The reviewer should be able to see assumptions, blockers, unresolved constraints, evidence sources, changes, and scenario differences rather than receiving only an opaque optimized answer.

## End-to-end reference workflow

A typical F112 workflow follows this sequence:

1. Capture demand, orders, priorities, planning horizon, and uncertainty.
2. Review routings, calendars, cycle times, setup assumptions, and available capacity.
3. Review materials, inventory, supplier dates, and lead times.
4. Register hard and soft constraints explicitly.
5. Build a candidate finite-capacity schedule.
6. Check precedence, resource, material, tooling, labor, and timing feasibility.
7. Review quality, safety, maintenance, calibration, and engineering dependencies.
8. Preserve evidence provenance and timestamps.
9. Compare alternative scenarios when useful.
10. Review material plan changes through change control.
11. Surface overload, shortages, lateness, and unresolved assumptions.
12. Apply fail-closed governance gates.
13. Require explicit qualified-human approval.
14. Keep schedule release, production authorization, inventory commitments, supplier commitments, constraint overrides, and quality or safety overrides outside autonomous authority.

## Explicit failure states

Useful explicit states include:

```text
DEMAND REVIEW INCOMPLETE
DEMAND UNCERTAINTY UNBOUNDED
CAPACITY REVIEW INCOMPLETE
CAPACITY OVERLOAD
MATERIAL SHORTAGE
LEAD TIME CONFLICT
INVENTORY INACCURATE
SCHEDULE INFEASIBLE
QUALITY HOLD ACTIVE
SAFETY HOLD ACTIVE
PLAN CHANGE UNREVIEWED
TRACEABILITY GAP
HUMAN APPROVAL REQUIRED
SCHEDULE RELEASE PROHIBITED
PRODUCTION AUTHORIZATION PROHIBITED
INVENTORY COMMITMENT PROHIBITED
SUPPLIER COMMITMENT PROHIBITED
CONSTRAINT OVERRIDE PROHIBITED
QUALITY OR SAFETY HOLD OVERRIDE PROHIBITED
```

F112 must never fabricate demand, capacity, inventory, supplier dates, quality release, safety clearance, approvals, material availability, or production authorization.

## Observability

The `observability/` layer supports traceability across the planning workflow.

Useful telemetry includes:

- demand-review state
- forecast uncertainty
- load and capacity
- bottlenecks
- shortages
- inventory confidence
- lead-time conflicts
- schedule feasibility
- quality and safety holds
- plan revisions
- human approval
- governance blockers
- protected-action attempts

Observability supports accountability and debugging. It does not create production authority.

## Memory and state

The `memory/` layer can preserve structured workflow context across agent stages.

State should distinguish source-system facts, forecasts, assumptions, calculations, proposed schedules, human overrides, approvals, and unresolved issues.

Stale or superseded state should not silently drive a new production recommendation.

## Versioning and change impact

Production planning should preserve versions of:

- demand
- forecasts
- orders
- BOM and routing
- inventory snapshot
- capacity calendar
- supplier commitments
- schedule
- constraints
- holds
- reviewer decisions

Material changes should trigger appropriate re-review rather than inheriting approval from an earlier plan.

## Evaluation and held-out governance suite

The repository contains evaluation logic under `evals/` and benchmark cases under `benchmarks/`.

Evaluation should test both planning usefulness and governance behavior, including:

- demand uncertainty handling
- capacity-overload detection
- material-shortage detection
- lead-time consistency
- inventory-accuracy enforcement
- schedule-feasibility detection
- quality and safety hold enforcement
- change-control enforcement
- traceability enforcement
- human-approval enforcement
- protected-action enforcement

The behavioral verification layer includes eight direct governance tests and a 10-scenario held-out production-planning suite.

## Verification gates

CI runs on Python 3.10, 3.11, and 3.12 and requires:

```bash
ruff check . --select E9,F63,F7,F82
python -m pytest -q
python evals/held_out.py
python run.py
```

These gates verify syntax-critical linting, fail-closed governance behavior, held-out production-planning scenarios, and execution of the governed reference workflow.

## Reproducibility

Install development dependencies:

```bash
python -m pip install -e .
```

Then run:

```bash
ruff check . --select E9,F63,F7,F82
python -m pytest -q
python evals/held_out.py
python run.py
```

## Extension points

Organization-specific implementations can add governed integrations for:

- ERP
- MRP
- MES
- advanced planning and scheduling systems
- warehouse-management systems
- supplier portals
- maintenance systems
- quality-management systems
- product lifecycle management
- workforce scheduling
- shop-floor data collection
- inventory systems

Integrations should preserve timestamps, provenance, access control, versioning, human authority, and fail-closed behavior.

## Example applications

Potential governed uses include:

- master production schedule support
- finite-capacity planning
- shortage analysis
- bottleneck analysis
- recovery planning
- schedule scenario comparison
- material-readiness review
- production meeting preparation
- planning training and simulation

F112 is not an autonomous production-control system, ERP authority, procurement authority, quality authority, safety authority, or substitute for qualified production planners.

## Design principles

F112 follows these principles:

1. Bound demand uncertainty before treating a plan as executable.
2. Use reviewed finite capacity rather than fictional resources.
3. Preserve material, inventory, supplier, and lead-time provenance.
4. Treat quality and safety holds as hard governance boundaries.
5. Expose shortages and infeasibility rather than hiding them.
6. Make plan changes and assumptions traceable.
7. Fail closed when required reviews or evidence are incomplete.
8. Keep schedule release, production authorization, commitments, and overrides under qualified human authority.

## Scope statement

F112 demonstrates a governed multi-agent architecture for production-planning support. It combines specialized demand, capacity, scheduling, materials, and review agents with deterministic planning tools, evidence traceability, observability, held-out evaluation, and fail-closed governance.

It is a reference implementation for governed production-planning workflow engineering, not a substitute for authorized planners, operations leaders, quality, safety, procurement, or supply-chain professionals.