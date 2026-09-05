"""Use a specialist as a tool when the manager must retain control."""

import asyncio

from _shared import MODEL, key_or_skip


async def main() -> None:
    if not key_or_skip():
        return
    from agents import Agent, Runner

    specialist = Agent(
        name="Policy reader",
        instructions="Answer only the policy question you receive.",
        model=MODEL,
    )
    manager = Agent(
        name="Support manager",
        instructions="Use the policy reader, then give the final customer response.",
        model=MODEL,
        tools=[
            specialist.as_tool(
                tool_name="read_policy", tool_description="Read policy guidance."
            )
        ],
    )
    result = await Runner.run(manager, "Can a customer cancel a subscription?")
    print("OK:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
