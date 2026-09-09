"""Serialize an interrupted SDK RunState and reconstruct it with the same agent tools."""

import asyncio
import json
import tempfile
from pathlib import Path

from _shared import demo_model, run_config
from agents import Agent, Runner, RunState, function_tool
from agents.testing import assistant_message, function_call


@function_tool(needs_approval=True)
def request_review() -> str:
    """Create a simulated review request."""
    return "Review requested."


def build_agent(resuming: bool = False) -> Agent[None]:
    steps = (
        [] if resuming else [[function_call("request_review", {}, call_id="review-1")]]
    )
    return Agent(
        name="Support",
        instructions="Call request_review, then report its outcome.",
        tools=[request_review],
        model=demo_model(
            *steps, [assistant_message("Review requested after approval.")]
        ),
    )


async def main() -> None:
    agent = build_agent()
    paused = await Runner.run(
        agent, "Request review.", max_turns=3, run_config=run_config()
    )
    if not paused.interruptions:
        raise RuntimeError("expected a pending approval")
    with tempfile.TemporaryDirectory() as directory:
        checkpoint = Path(directory) / "run.json"
        checkpoint.write_text(json.dumps(paused.to_state().to_json()))
        restored_agent = build_agent(resuming=True)
        state = await RunState.from_json(
            restored_agent, json.loads(checkpoint.read_text())
        )
        for item in state.get_interruptions():
            state.approve(item)
        result = await Runner.run(restored_agent, state, run_config=run_config())
    print("OK: resumed SDK state:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
