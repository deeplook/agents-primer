"""Let a triage agent hand a task to a specialist that takes control."""

import asyncio

from _shared import MODEL, key_or_skip


async def main() -> None:
    if not key_or_skip():
        return
    from agents import Agent, Runner

    billing = Agent(
        name="Billing specialist",
        handoff_description="Handles invoices and refunds.",
        instructions="Answer billing questions in one sentence.",
        model=MODEL,
    )
    triage = Agent(
        name="Triage",
        instructions="Hand billing questions to the Billing specialist.",
        model=MODEL,
        handoffs=[billing],
    )
    result = await Runner.run(triage, "I need a refund for my invoice.")
    print(f"OK: agent={result.last_agent.name} output={result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
