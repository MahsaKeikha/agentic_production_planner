"""Fail-closed governance for F112 Production Planner."""

PROTECTED_ACTIONS = {
    "release_schedule",
    "override_constraint",
    "commit_inventory",
    "authorize_production",
    "expedite_supplier_commitment",
    "override_quality_or_safety_hold",
}

REQUIRED_REVIEWS = (
    "demand_reviewed",
    "capacity_reviewed",
    "materials_reviewed",
    "schedule_reviewed",
    "inventory_reviewed",
    "quality_safety_dependencies_reviewed",
    "change_control_reviewed",
    "human_approval",
)


def authorize(action: str, context: dict | None = None) -> dict:
    context = context or {}
    if action in PROTECTED_ACTIONS:
        return {"allowed": False, "reason": "binding production authority is outside reference-system scope"}

    missing = [key for key in REQUIRED_REVIEWS if not context.get(key)]
    if missing:
        return {"allowed": False, "reason": "missing required production-planning review", "missing": missing}

    blockers = []
    if context.get("demand_uncertainty_unbounded"):
        blockers.append("demand uncertainty is not adequately bounded")
    if context.get("capacity_overload"):
        blockers.append("planned load exceeds reviewed capacity")
    if context.get("material_shortage"):
        blockers.append("required material shortage unresolved")
    if context.get("lead_time_conflict"):
        blockers.append("lead-time assumptions conflict with schedule")
    if context.get("inventory_inaccuracy"):
        blockers.append("inventory accuracy or availability is unresolved")
    if context.get("schedule_infeasible"):
        blockers.append("production schedule is infeasible")
    if context.get("quality_safety_hold"):
        blockers.append("quality or safety dependency blocks production")
    if context.get("unreviewed_plan_change"):
        blockers.append("material planning change lacks change-control review")
    if context.get("traceability_gap"):
        blockers.append("planning inputs or decisions are not traceable")

    if blockers:
        return {"allowed": False, "reason": "production-planning governance blocker", "blockers": blockers}

    return {"allowed": True, "reason": "planning recommendation approved after qualified human review"}
