from orchestration.orchestrator import orchestrate
from safety.policy import authorize


def valid_context():
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


def test_complete_review_can_release_planning_recommendation():
    result = orchestrate(valid_context())
    assert result["release_allowed"] is True
    assert result["autonomous_schedule_release_authority"] is False


def test_missing_human_approval_fails_closed():
    context = valid_context()
    context["human_approval"] = False
    assert orchestrate(context)["release_allowed"] is False


def test_schedule_release_is_never_autonomous():
    assert authorize("release_schedule", valid_context())["allowed"] is False


def test_capacity_overload_blocks_release():
    context = valid_context()
    context["capacity_overload"] = True
    assert orchestrate(context)["release_allowed"] is False


def test_material_shortage_blocks_release():
    context = valid_context()
    context["material_shortage"] = True
    assert orchestrate(context)["release_allowed"] is False


def test_schedule_infeasibility_blocks_release():
    context = valid_context()
    context["schedule_infeasible"] = True
    assert orchestrate(context)["release_allowed"] is False


def test_quality_safety_hold_blocks_release():
    context = valid_context()
    context["quality_safety_hold"] = True
    assert orchestrate(context)["release_allowed"] is False


def test_traceability_gap_blocks_release():
    context = valid_context()
    context["traceability_gap"] = True
    assert orchestrate(context)["release_allowed"] is False
