from AGENTS.demand_agent import run as a1
from AGENTS.capacity_agent import run as a2
from AGENTS.scheduling_agent import run as a3
from AGENTS.materials_agent import run as a4
from AGENTS.reviewer_agent import run as a5
def orchestrate(c): return [a(c) for a in (a1,a2,a3,a4,a5)]