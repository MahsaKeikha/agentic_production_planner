from orchestration.orchestrator import orchestrate
def test_orchestrator(): assert len(orchestrate({"objective":"x","context":{}}))==5