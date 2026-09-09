"""Two SDK agents read the same immutable local context through typed tools."""

import asyncio
from dataclasses import dataclass

from _shared import demo_model, run_config
from agents import Agent, RunContextWrapper, Runner, function_tool
from agents.testing import assistant_message, function_call


@dataclass(frozen=True)
class Brief:
    account: str
    issue: str
    policy_version: str


@function_tool
def read_brief(ctx: RunContextWrapper[Brief]) -> str:
    """Read the shared brief; local context is not automatically a model prompt."""
    return f"{ctx.context.account}: {ctx.context.issue}; policy={ctx.context.policy_version}"


async def main() -> None:
    brief = Brief("Ada", "duplicate charge", "2026-01")
    agents = [
        Agent[Brief](
            name=name,
            instructions="Read the shared brief and report your finding.",
            tools=[read_brief],
            model=demo_model(
                [function_call("read_brief", {}, call_id=f"{name}-brief")],
                [assistant_message(f"{name}: duplicate charge under policy 2026-01.")],
            ),
        )
        for name in ("Ledger", "Policy")
    ]
    results = await asyncio.gather(
        *[
            Runner.run(
                agent,
                "Review your part.",
                context=brief,
                max_turns=3,
                run_config=run_config(),
            )
            for agent in agents
        ]
    )
    print(f"OK: shared_context={brief} findings={[r.final_output for r in results]}")


if __name__ == "__main__":
    asyncio.run(main())
