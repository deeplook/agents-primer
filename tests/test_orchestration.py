"""Exercise control-flow contracts with deterministic responses, without credits."""

import asyncio
import importlib
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest
from agents import ModelBehaviorError

sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))
from _orchestration import Plan, Task


def lesson(name: str) -> Any:
    return importlib.import_module(name)


@pytest.mark.parametrize(
    "tasks",
    [
        [],
        [Task(id="a", action="read_invoice"), Task(id="a", action="read_invoice")],
        [Task(id="a", action="send_money")],
        [Task(id="a", action="read_invoice", depends_on=["missing"])],
        [Task(id="a", action="read_invoice", depends_on=["a"])],
    ],
)
def test_invalid_plan_executes_nothing(
    tasks: list[Task], monkeypatch: pytest.MonkeyPatch
) -> None:
    module = lesson("11_plan_execute")
    calls: list[str] = []
    monkeypatch.setitem(module.ACTIONS, "read_invoice", lambda: calls.append("called"))
    with pytest.raises(ValueError):
        module.execute(Plan(tasks=tasks))
    assert calls == []


def test_forward_dependency_rejected_before_actions() -> None:
    plan = Plan(
        tasks=[
            Task(id="a", action="read_invoice", depends_on=["b"]),
            Task(id="b", action="check_policy"),
        ]
    )
    with pytest.raises(ValueError, match="forward dependency"):
        lesson("11_plan_execute").execute(plan)


def test_refinement_accepts_or_returns_unapproved_candidate() -> None:
    module = lesson("10_evaluator_refiner")
    assert asyncio.run(module.revise())[1] == "accepted"
    assert asyncio.run(module.revise(limit=1))[1] == "budget_exhausted"


def test_refinement_stagnation(monkeypatch: pytest.MonkeyPatch) -> None:
    module = lesson("10_evaluator_refiner")

    async def scripted(name: str, *_: Any) -> Any:
        if name == "Writer":
            return module.Draft(text="Unchanged draft")
        return module.Critique(accepted=False, score=2, issues=["Needs revision"])

    monkeypatch.setattr(module, "ask", scripted)
    assert asyncio.run(module.revise()) == ("Unchanged draft", "stalled")


def test_partial_failure_preserves_evidence() -> None:
    module = lesson("42_partial_failure")
    findings, status = asyncio.run(module.collect())
    assert set(findings) == {"ledger"}
    assert status.startswith("partial")
    assert asyncio.run(module.collect(required="policy"))[1].startswith("blocked")


def test_dependencies_wait_for_parents(monkeypatch: pytest.MonkeyPatch) -> None:
    module = lesson("43_dependency_scheduling")
    received: dict[str, dict[str, str]] = {}

    async def execute(task: Task, inputs: dict[str, str]) -> str:
        received[task.id] = inputs
        await asyncio.sleep(0)
        return task.id + " result"

    monkeypatch.setattr(module, "execute", execute)
    plan = Plan(
        tasks=[
            Task(id="a", action="read_invoice"),
            Task(id="b", action="check_policy"),
            Task(id="c", action="summarize", depends_on=["a", "b"]),
        ]
    )
    assert len(asyncio.run(module.schedule(plan))) == 3
    assert received["c"] == {"a": "a result", "b": "b result"}


def test_failed_wave_cancels_sibling_and_never_starts_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = lesson("43_dependency_scheduling")
    cancelled: list[str] = []
    started: list[str] = []

    async def scenario() -> None:
        ready = asyncio.Event()

        async def execute(task: Task, inputs: dict[str, str]) -> str:
            started.append(task.id)
            if task.id == "a":
                await ready.wait()
                raise TimeoutError("injected")
            ready.set()
            try:
                await asyncio.Event().wait()
            finally:
                cancelled.append(task.id)
            return "unreachable"

        monkeypatch.setattr(module, "execute", execute)
        plan = Plan(
            tasks=[
                Task(id="a", action="read_invoice"),
                Task(id="b", action="check_policy"),
                Task(id="c", action="summarize", depends_on=["a", "b"]),
            ]
        )
        with pytest.raises(ExceptionGroup):
            await module.schedule(plan)

    asyncio.run(scenario())
    assert set(started) == {"a", "b"}
    assert cancelled == ["b"]


def test_replan_does_not_replay_completed_work(monkeypatch: pytest.MonkeyPatch) -> None:
    module = lesson("44_replanning")
    calls: list[str] = []
    original = module.execute

    def execute(action: str) -> str:
        calls.append(action)
        return str(original(action))

    monkeypatch.setattr(module, "execute", execute)
    assert set(asyncio.run(module.resolve())) == {"invoice", "human"}
    assert calls == ["read_invoice", "lookup_policy", "queue_review"]


@pytest.mark.parametrize(
    "action, message",
    [("read_invoice", "unfinished"), ("lookup_policy", "budget exhausted")],
)
def test_replan_rejects_replay_and_stops_retry(
    action: str, message: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = lesson("44_replanning")

    async def scripted(*_: Any) -> Plan:
        return Plan(tasks=[Task(id="replacement", action=action)])

    monkeypatch.setattr(module, "ask", scripted)
    with pytest.raises((ValueError, RuntimeError), match=message):
        asyncio.run(module.resolve())


def test_approval_survives_process_restart(tmp_path: Path) -> None:
    script = Path(__file__).parent.parent / "examples/45_approval_resume.py"
    for command, expected in [
        ("prepare", "('pending', 0)"),
        ("approve", "('executed', 1)"),
        ("approve", "('executed', 1)"),
    ]:
        result = subprocess.run(
            [
                sys.executable,
                str(script),
                command,
                "--db",
                str(tmp_path / "approval.sqlite"),
            ],
            capture_output=True,
            text=True,
            check=True,
            env=os.environ | {"OPENAI_API_KEY": ""},
        )
        assert expected in result.stdout


def test_rejection_is_terminal(tmp_path: Path) -> None:
    transition = lesson("45_approval_resume").transition
    path = tmp_path / "approval.sqlite"
    with pytest.raises(ValueError, match="prepare"):
        transition(path, "approve")
    assert transition(path, "prepare") == ("pending", 0)
    assert transition(path, "reject") == ("rejected", 0)
    assert transition(path, "approve") == ("rejected", 0)


def test_scripted_output_is_validated() -> None:
    module = lesson("_orchestration")
    with pytest.raises(ModelBehaviorError):
        asyncio.run(module.ask("planner", "", "", Plan, {"tasks": "invalid"}))


def test_live_boundary_uses_typed_agent_and_turn_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = lesson("_orchestration")
    response = Plan(tasks=[Task(id="invoice", action="read_invoice")])
    run = AsyncMock(return_value=SimpleNamespace(final_output=response))
    monkeypatch.setattr(sys, "argv", ["example", "--live"])
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-no-network")
    monkeypatch.setattr(module.Runner, "run", run)
    result = asyncio.run(module.ask("Planner", "Plan review", "Order 42", Plan, {}))
    assert result == response
    agent, prompt = run.call_args.args
    assert agent.output_type is Plan
    assert prompt == "Order 42"
    assert run.call_args.kwargs["max_turns"] == 3
    assert not run.call_args.kwargs["run_config"].tracing_disabled


def test_parallel_findings_reach_synthesizer(monkeypatch: pytest.MonkeyPatch) -> None:
    module = lesson("08_fan_out")

    async def scenario() -> None:
        started: set[str] = set()
        both_started = asyncio.Event()

        async def scripted(
            name: str, instructions: str, prompt: str, *args: Any
        ) -> Any:
            if name == "Support":
                assert "Ledger evidence" in prompt and "Policy evidence" in prompt
                return module.Reply(text="Combined")
            started.add(name)
            if len(started) == 2:
                both_started.set()
            await asyncio.wait_for(both_started.wait(), timeout=1)
            return module.Finding(evidence=f"{name} evidence")

        monkeypatch.setattr(module, "ask", scripted)
        assert (await module.investigate()).text == "Combined"

    asyncio.run(scenario())
