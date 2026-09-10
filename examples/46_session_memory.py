"""SQLiteSession accumulates conversation history automatically across Runner.run calls."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.memory import SQLiteSession
from agents.testing import assistant_message


async def main() -> None:
    agent = Agent(
        name="Assistant",
        instructions="Answer briefly using only the conversation so far.",
        model=demo_model(
            [assistant_message("Nice to meet you, Ana.")],
            [assistant_message("Your name is Ana.")],
        ),
    )
    session = SQLiteSession("demo-session")
    try:
        first = await Runner.run(
            agent,
            "My name is Ana.",
            max_turns=3,
            run_config=run_config(),
            session=session,
        )
        second = await Runner.run(
            agent,
            "What's my name?",
            max_turns=3,
            run_config=run_config(),
            session=session,
        )
        stored = await session.get_items()
    finally:
        session.close()
    print(
        f"OK: first={first.final_output!r} second={second.final_output!r} "
        f"stored_items={len(stored)}"
    )


if __name__ == "__main__":
    asyncio.run(main())
