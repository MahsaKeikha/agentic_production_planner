from AGENTS.capacity_agent import run as capacity
from AGENTS.demand_agent import run as demand
from AGENTS.materials_agent import run as materials
from AGENTS.reviewer_agent import run as reviewer
from AGENTS.scheduling_agent import run as scheduling
from safety.policy import authorize


def orchestrate(context: dict) -> dict:
    """Run planning specialists and apply fail-closed production governance."""
    results = [
        demand(context),
        capacity(context),
        scheduling(context),
        materials(context),
        reviewer(context),
    ]
    governance = authorize("planning_release", context)
    return {
        "system": "F112",
        "results": results,
        "governance": governance,
        "release_allowed": governance["allowed"],
        "human_review_required": True,
        "autonomous_schedule_release_authority": False,
        "autonomous_inventory_commitment_authority": False,
        "autonomous_constraint_override_authority": False,
    }
