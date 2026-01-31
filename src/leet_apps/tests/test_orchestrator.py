from leet_apps.orchestrator import Orchestrator, run_for_fund


def test_orchestrator_runs_basic():
    orch = Orchestrator()
    res = orch.run("Sequoia Capital")
    assert "fund" in res
    assert "companies" in res
    assert isinstance(res["companies"], list)
    # run convenience
    r2 = run_for_fund("Sequoia Capital")
    assert "fund" in r2
