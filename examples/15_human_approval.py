"""SDK needs_approval interrupts a tool call; RunState approves or rejects it."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner, function_tool
from agents.testing import assistant_message, function_call


async def review(approved: bool) -> int:
    ledger: list[str] = []

    @function_tool(needs_approval=True)
    def issue_refund() -> str:
        """Record a simulated refund; no external payment is made."""
        ledger.append("refund")
        return "Simulated refund recorded."

    agent = Agent(
        name="Refunds",
        instructions="Call issue_refund, then report its outcome.",
        tools=[issue_refund],
        model=demo_model(
            [function_call("issue_refund", {}, call_id="refund-1")],
            [assistant_message("Approval decision processed.")],
        ),
    )
    paused = await Runner.run(
        agent, "Refund the duplicate.", max_turns=3, run_config=run_config()
    )
    if not paused.interruptions:
        raise RuntimeError("model did not request the approval-required tool")
    assert not ledger
    state = paused.to_state()
    for item in paused.interruptions:
        if approved:
            state.approve(item)
        else:
            state.reject(item)
    result = await Runner.run(agent, state, run_config=run_config())
    print(f"OK: approved={approved} effects={len(ledger)} output={result.final_output}")
    return len(ledger)


async def main() -> None:
    await review(False)
    await review(True)


if __name__ == "__main__":
    asyncio.run(main())
