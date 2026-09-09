"""An SDK handoff transfers ownership of the final reply to a specialist."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message, function_call


async def main() -> None:
    billing = Agent(
        name="Billing",
        instructions="Answer billing questions briefly.",
        model=demo_model([assistant_message("I can help review your refund.")]),
    )
    triage = Agent(
        name="Triage",
        instructions="Hand billing requests to Billing.",
        handoffs=[billing],
        model=demo_model(
            [function_call("transfer_to_billing", {}, call_id="handoff-1")]
        ),
    )
    result = await Runner.run(
        triage, "I need a refund.", max_turns=3, run_config=run_config()
    )
    print(f"OK: owner={result.last_agent.name} output={result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
