"""Test real SDK behavior with ScriptedModel; no provider requests or trace export."""

import asyncio
import importlib
import sys
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))

from _shared import demo_model, run_config
from agents import (
    Agent,
    InputGuardrailTripwireTriggered,
    MaxTurnsExceeded,
    ModelBehaviorError,
    OutputGuardrailTripwireTriggered,
    Runner,
)
from agents.testing import ScriptedModel, assistant_message, function_call


def lesson(name: str) -> Any:
    return importlib.import_module(name)


def test_sdk_input_guardrail_prevents_model_call() -> None:
    model = ScriptedModel([[assistant_message("must not run")]])
    agent = Agent(
        name="Support",
        model=model,
        input_guardrails=[lesson("14_input_guardrail").scope],
    )
    with pytest.raises(InputGuardrailTripwireTriggered):
        asyncio.run(
            Runner.run(agent, "Please delete account.", run_config=run_config())
        )
    assert not model.calls


def test_sdk_output_guardrail() -> None:
    model = ScriptedModel([[assistant_message("Answer: internal record.")]])
    agent = Agent(
        name="Support",
        model=model,
        output_guardrails=[lesson("22_output_guardrail").delivery],
    )
    with pytest.raises(OutputGuardrailTripwireTriggered):
        asyncio.run(Runner.run(agent, "Reply", run_config=run_config()))
    assert len(model.calls) == 1


def test_sdk_turn_limit() -> None:
    module = lesson("06_bounded_loop")
    model = ScriptedModel(
        [[function_call("inspect_again", {}, call_id=f"call-{i}")] for i in range(3)]
    )
    agent = Agent(name="Loop", model=model, tools=[module.inspect_again])
    with pytest.raises(MaxTurnsExceeded):
        asyncio.run(Runner.run(agent, "Inspect", max_turns=2, run_config=run_config()))
    assert len(model.calls) == 2


def test_sdk_rejects_unknown_tool() -> None:
    agent = Agent(
        name="Read only",
        model=demo_model([function_call("issue_refund", {}, call_id="overreach")]),
        tools=[lesson("39_tool_access").search_documents],
    )
    with pytest.raises(ModelBehaviorError):
        asyncio.run(Runner.run(agent, "Refund", run_config=run_config()))


def test_sdk_approval_gates_actual_tool_execution() -> None:
    review = lesson("15_human_approval").review
    assert asyncio.run(review(False)) == 0
    assert asyncio.run(review(True)) == 1


def test_sdk_manager_delegates_twice(monkeypatch: pytest.MonkeyPatch) -> None:
    module = lesson("25_manager_worker")
    models: list[ScriptedModel] = []

    def tracked(*steps: Any) -> ScriptedModel:
        model = ScriptedModel(steps)
        models.append(model)
        return model

    monkeypatch.setattr(module, "demo_model", tracked)
    owner, decision = asyncio.run(module.manage())
    worker, manager = models
    assert len(worker.calls) == 2 and len(manager.calls) == 3
    assert owner == "Support manager" and decision.next_step == "human review"
    assert "Need the order ID" in str(manager.calls[1].input)
    assert "two identical charges" in str(manager.calls[2].input)


def test_sdk_context_tool_updates_local_state() -> None:
    module = lesson("05_typed_state")
    account = module.Account(customer="Ada")
    model = ScriptedModel(
        [
            [function_call("read_account", {}, call_id="read")],
            [assistant_message("Hello Ada.")],
        ]
    )
    agent = Agent(name="Support", model=model, tools=[module.read_account])
    asyncio.run(
        Runner.run(agent, "Who am I?", context=account, run_config=run_config())
    )
    assert account.notes == ["account read"]
    assert "Ada" not in str(model.calls[0].input)
    assert "Ada" in str(model.calls[1].input)


def test_sdk_routing_eval() -> None:
    records = asyncio.run(lesson("_evaluation").evaluate())
    assert len(records) == 3
    assert all(
        expected == actual and turns == 1 for _, expected, actual, turns in records
    )


def test_sdk_capstone_approval_and_rejection() -> None:
    handle = lesson("29_capstone_triage").handle
    assert asyncio.run(handle("delete account")) == "rejected:input"
    assert "effects=0" in asyncio.run(handle("Refund please", False))
    assert "owner=Billing approved=True effects=1" == asyncio.run(
        handle("Refund please", True)
    )


def test_sdk_checkpoint_restores_approval(tmp_path: Path) -> None:
    import json

    from agents import RunState

    module = lesson("20_checkpoint_resume")

    async def scenario() -> None:
        original = module.build_agent()
        paused = await Runner.run(original, "Request review", run_config=run_config())
        checkpoint = tmp_path / "run.json"
        checkpoint.write_text(json.dumps(paused.to_state().to_json()))
        restored = module.build_agent(resuming=True)
        state = await RunState.from_json(restored, json.loads(checkpoint.read_text()))
        assert len(state.get_interruptions()) == 1
        state.approve(state.get_interruptions()[0])
        resumed = await Runner.run(restored, state, run_config=run_config())
        assert not resumed.interruptions
        assert any(item.type == "tool_call_output_item" for item in resumed.new_items)

    asyncio.run(scenario())


def test_offline_remains_scripted_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-be-used")
    assert isinstance(demo_model([assistant_message("offline")]), ScriptedModel)
    assert run_config().tracing_disabled


def test_sdk_tool_failure_routes_to_recovery(
    capsys: pytest.CaptureFixture[str],
) -> None:
    asyncio.run(lesson("24_failure_edges").main())
    assert "edge=Recovery" in capsys.readouterr().out
