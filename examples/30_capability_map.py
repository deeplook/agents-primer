"""Build SDK specialists from concrete tool capabilities, then delegate via handoff."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner, function_tool
from agents.testing import assistant_message, function_call


@function_tool
def search_documents() -> str:
    """Read the public refund policy."""
    return "Duplicates qualify for review."


@function_tool(needs_approval=True)
def request_refund_approval() -> str:
    """Record a simulated request for refund review."""
    return "Review requested."


async def main() -> None:
    research = Agent(
        name="Research",
        instructions="Read policy with search_documents.",
        tools=[search_documents],
        model=demo_model(
            [function_call("search_documents", {}, call_id="search-1")],
            [assistant_message("Duplicates qualify for review.")],
        ),
    )
    resolution = Agent(
        name="Resolution", tools=[request_refund_approval], model=demo_model()
    )
    router = Agent(
        name="Router",
        instructions="Route policy questions to Research.",
        handoffs=[research, resolution],
        model=demo_model(
            [function_call("transfer_to_research", {}, call_id="route-1")]
        ),
    )
    result = await Runner.run(
        router, "What is the refund policy?", max_turns=4, run_config=run_config()
    )
    print(f"OK: owner={result.last_agent.name} output={result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
