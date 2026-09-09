"""Pass typed local context to an SDK tool; it is not automatically model history."""

import asyncio
from dataclasses import dataclass, field

from _shared import demo_model, run_config
from agents import Agent, RunContextWrapper, Runner, function_tool
from agents.testing import assistant_message, function_call


@dataclass
class Account:
    customer: str
    notes: list[str] = field(default_factory=list)


@function_tool
def read_account(ctx: RunContextWrapper[Account]) -> str:
    """Read the account associated with this run."""
    ctx.context.notes.append("account read")
    return f"Customer: {ctx.context.customer}"


async def main() -> None:
    account = Account(customer="Ada")
    agent = Agent[Account](
        name="Support",
        instructions="Read the account, then greet the customer.",
        tools=[read_account],
        model=demo_model(
            [function_call("read_account", {}, call_id="account-1")],
            [assistant_message("Hello Ada.")],
        ),
    )
    result = await Runner.run(
        agent, "Who am I?", context=account, run_config=run_config(), max_turns=3
    )
    print(f"OK: output={result.final_output} local_notes={account.notes}")


if __name__ == "__main__":
    asyncio.run(main())
