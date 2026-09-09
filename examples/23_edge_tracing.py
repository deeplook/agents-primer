"""SDK lifecycle hooks record handoffs; trace groups the entire workflow."""

import asyncio
from typing import Any

from _shared import demo_model, live, run_config
from agents import Agent, RunContextWrapper, RunHooks, Runner, trace
from agents.testing import assistant_message, function_call


class Edges(RunHooks[None]):
    def __init__(self) -> None:
        self.edges: list[tuple[str, str]] = []

    async def on_handoff(
        self,
        context: RunContextWrapper[None],
        from_agent: Agent[Any],
        to_agent: Agent[Any],
    ) -> None:
        self.edges.append((from_agent.name, to_agent.name))


async def main() -> None:
    billing = Agent(
        name="Billing", model=demo_model([assistant_message("Review requested.")])
    )
    triage = Agent(
        name="Triage",
        instructions="Transfer billing questions to Billing.",
        handoffs=[billing],
        model=demo_model([function_call("transfer_to_billing", {}, call_id="edge-1")]),
    )
    hooks = Edges()
    with trace("support-triage", disabled=not live()):
        await Runner.run(
            triage,
            "Refund my invoice.",
            hooks=hooks,
            run_config=run_config(),
            max_turns=3,
        )
    print(f"OK: SDK handoff events={hooks.edges}")


if __name__ == "__main__":
    asyncio.run(main())
