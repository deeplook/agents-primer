"""The SDK executes a typed function tool and returns its result to the model."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner, function_tool
from agents.testing import assistant_message, function_call


@function_tool
def lookup_priority(customer: str) -> str:
    """Return a customer's support priority."""
    return {"Ada": "high", "Bea": "normal"}.get(customer, "normal")


async def main() -> None:
    agent = Agent(
        name="Triage",
        instructions="Look up Ada's priority, then answer.",
        tools=[lookup_priority],
        model=demo_model(
            [
                function_call(
                    "lookup_priority", {"customer": "Ada"}, call_id="priority-1"
                )
            ],
            [assistant_message("Ada has high priority.")],
        ),
    )
    result = await Runner.run(
        agent, "What priority should Ada receive?", max_turns=3, run_config=run_config()
    )
    print(
        "OK:", result.final_output, "items=", [item.type for item in result.new_items]
    )


if __name__ == "__main__":
    asyncio.run(main())
