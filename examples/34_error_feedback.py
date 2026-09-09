"""SDK function-tool error handling returns scoped feedback for another model turn."""

import asyncio
from typing import Any

from _shared import demo_model, run_config
from agents import Agent, RunContextWrapper, Runner, function_tool
from agents.testing import assistant_message, function_call


def feedback(ctx: RunContextWrapper[Any], error: Exception) -> str:
    # Avoid exposing raw exception text or internal identifiers.
    return "Account not found. Ask the user to verify their account ID."


@function_tool(failure_error_function=feedback)
def lookup_account(account_id: str) -> str:
    """Look up an account (this demo always fails)."""
    raise LookupError("internal backend record missing")


async def main() -> None:
    agent = Agent(
        name="Support",
        instructions="Look up the account; use tool feedback to recover.",
        tools=[lookup_account],
        model=demo_model(
            [
                function_call(
                    "lookup_account", {"account_id": "missing"}, call_id="lookup-1"
                )
            ],
            [assistant_message("Please verify your account ID.")],
        ),
    )
    result = await Runner.run(
        agent, "Check account missing.", max_turns=3, run_config=run_config()
    )
    outputs = [
        item.output for item in result.new_items if item.type == "tool_call_output_item"
    ]
    print(f"OK: tool_feedback={outputs} reply={result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
