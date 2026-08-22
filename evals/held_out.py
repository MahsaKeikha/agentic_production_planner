from orchestration.orchestrator import orchestrate


def base():
    return {
        "demand_reviewed": True,
        "capacity_reviewed": True,
        "materials_reviewed": True,
        "schedule_reviewed": True,
        "inventory_reviewed": True,
        "quality_safety_dependencies_reviewed": True,
        "change_control_reviewed": True,
        "human_approval": True,
    }


SCENARIOS = [
    ({}, False),
    (base(), True),
    ({**base(), "human_approval": False}, False),
    ({**base(), "demand_uncertainty_unbounded": True}, False),
    ({**base(), "capacity_overload": True}, False),
    ({**base(), "material_shortage": True}, False),
    ({**base(), "lead_time_conflict": True}, False),
    ({**base(), "inventory_inaccuracy": True}, False),
    ({**base(), "quality_safety_hold": True}, False),
    ({**base(), "unreviewed_plan_change": True}, False),
]


def main():
    passed = 0
    for context, expected in SCENARIOS:
        passed += orchestrate(context)["release_allowed"] is expected
    print(f"held-out: {passed}/{len(SCENARIOS)} passed")
    raise SystemExit(0 if passed == len(SCENARIOS) else 1)


if __name__ == "__main__":
    main()
