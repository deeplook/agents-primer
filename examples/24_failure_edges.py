"""A function-tool exception escapes the SDK and selects a Python recovery edge."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner, UserError, function_tool
from agents.testing import assistant_message, function_call


@function_tool(failure_error_function=None)
def lookup_account(account_id: str) -> str:
    """Look up an account; the demo ID 'missing' raises LookupError."""
    if account_id == "missing":
        raise LookupError("account unavailable")
    return "active"


async def main() -> None:
    lookup = Agent(
        name="Lookup",
        instructions="Call lookup_account with the supplied ID.",
        tools=[lookup_account],
        model=demo_model(
            [
                function_call(
                    "lookup_account", {"account_id": "missing"}, call_id="lookup-1"
                )
            ]
        ),
    )
    try:
        result = await Runner.run(
            lookup, "Account ID: missing", max_turns=3, run_config=run_config()
        )
    except UserError as error:
        # The SDK wraps tool exceptions; recover only the expected cause.
        if not isinstance(error.__cause__, LookupError):
            raise
        recovery = Agent(
            name="Recovery",
            instructions="Ask for a valid account ID.",
            model=demo_model([assistant_message("Please check your account ID.")]),
        )
        result = await Runner.run(
            recovery, "Account lookup failed.", max_turns=3, run_config=run_config()
        )
    print(f"OK: edge={result.last_agent.name} output={result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
