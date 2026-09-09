"""SDK tool exposure is per agent; a hidden tool cannot execute even if requested."""

import asyncio

from _shared import demo_model, live, run_config
from agents import Agent, ModelBehaviorError, Runner, function_tool
from agents.testing import assistant_message, function_call


@function_tool
def search_documents() -> str:
    """Read public policy."""
    return "Duplicates qualify for review."


async def main() -> None:
    agent = Agent(
        name="Research",
        instructions="Read policy. You cannot issue refunds.",
        tools=[search_documents],
        model=demo_model([function_call("issue_refund", {}, call_id="overreach-1")]),
    )
    # Offline deliberately fabricates an unavailable tool call to test enforcement.
    if live():
        agent.model = demo_model([assistant_message("No refund capability.")])
    try:
        result = await Runner.run(
            agent, "Issue a refund.", max_turns=3, run_config=run_config()
        )
        print("OK: only search_documents exposed:", result.final_output)
    except ModelBehaviorError:
        print("OK: SDK rejected an unknown tool; no refund tool exists on this agent")


if __name__ == "__main__":
    asyncio.run(main())
