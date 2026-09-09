"""Python retries a failed SDK run twice, then runs a fallback agent."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message


async def main() -> None:
    primary = Agent(
        name="Primary",
        instructions="Give concise support guidance.",
        model=demo_model(TimeoutError("injected"), TimeoutError("injected")),
    )
    for attempt in range(1, 3):
        try:
            result = await Runner.run(
                primary, "Help with an invoice.", run_config=run_config(), max_turns=3
            )
            break
        except TimeoutError:
            print(f"attempt={attempt}: timed out")
    else:
        fallback = Agent(
            name="Fallback",
            instructions="Explain how to request human support.",
            model=demo_model([assistant_message("Request human review.")]),
        )
        result = await Runner.run(
            fallback,
            "Primary service failed twice.",
            run_config=run_config(),
            max_turns=3,
        )
    print(f"OK: agent={result.last_agent.name} output={result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
