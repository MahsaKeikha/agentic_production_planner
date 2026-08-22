from orchestration.orchestrator import orchestrate

REFERENCE_CONTEXT = {
    "objective": "build a feasible production plan",
    "demand_reviewed": True,
    "capacity_reviewed": True,
    "materials_reviewed": True,
    "schedule_reviewed": True,
    "inventory_reviewed": True,
    "quality_safety_dependencies_reviewed": True,
    "change_control_reviewed": True,
    "human_approval": True,
}

if __name__ == "__main__":
    print(orchestrate(REFERENCE_CONTEXT))
