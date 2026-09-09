"""Compose SDK input guardrails, specialist handoff, and tool approval/resumption."""

import asyncio
from typing import Any

from _shared import demo_model, run_config
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    function_tool,
    input_guardrail,
)
from agents.testing import assistant_message, function_call


@input_guardrail(run_in_parallel=False)
def scope(
    ctx: RunContextWrapper[None],
    agent: Agent[Any],
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    return GuardrailFunctionOutput(
        output_info="support only",
        tripwire_triggered=not isinstance(input, str)
        or "delete account" in input.lower(),
    )


async def handle(request: str, approved: bool = False) -> str:
    effects: list[str] = []

    @function_tool(needs_approval=True)
    def queue_refund() -> str:
        """Record a simulated refund review."""
        effects.append("queued")
        return "Review queued."

    billing = Agent(
        name="Billing",
        instructions="Call queue_refund then report the outcome.",
        tools=[queue_refund],
        model=demo_model(
            [function_call("queue_refund", {}, call_id="queue-1")],
            [assistant_message("Review decision processed.")],
        ),
    )
    triage = Agent(
        name="Triage",
        instructions="Transfer refund requests to Billing.",
        input_guardrails=[scope],
        handoffs=[billing],
        model=demo_model([function_call("transfer_to_billing", {}, call_id="route-1")]),
    )
    try:
        result = await Runner.run(triage, request, max_turns=4, run_config=run_config())
    except InputGuardrailTripwireTriggered:
        return "rejected:input"
    if not result.interruptions:
        raise RuntimeError("expected specialist approval request")
    state = result.to_state()
    for item in result.interruptions:
        state.approve(item) if approved else state.reject(item)
    result = await Runner.run(triage, state, run_config=run_config())
    return f"owner={result.last_agent.name} approved={approved} effects={len(effects)}"


async def main() -> None:
    for request, approved in [
        ("Please delete account.", False),
        ("Review my refund.", False),
        ("Review my refund.", True),
    ]:
        print("OK:", await handle(request, approved))


if __name__ == "__main__":
    asyncio.run(main())
