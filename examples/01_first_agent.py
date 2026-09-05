"""Define one focused agent and run a single turn."""

import asyncio

from _shared import MODEL, key_or_skip


async def main() -> None:
    if not key_or_skip():
        return
    from agents import Agent, Runner

    agent = Agent(
        name="Concise tutor",
        instructions="Answer in one concise sentence.",
        model=MODEL,
    )
    result = await Runner.run(agent, "What is a workflow graph?")
    print("OK:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
