"""An asyncio deadline cancels an SDK run, including its in-flight model wait."""

import asyncio

from _shared import demo_model, live, run_config
from agents import Agent, Runner
from agents.testing import ModelCall, ModelStep


async def unavailable(call: ModelCall) -> ModelStep:
    await asyncio.Event().wait()  # Offline failure injection at the model boundary.
    raise AssertionError("unreachable")


async def main() -> None:
    agent = Agent(
        name="Researcher",
        instructions="Explain SQL briefly.",
        model=demo_model(ModelStep.respond(unavailable)),
    )
    budget = 30 if live() else 0.01
    try:
        async with asyncio.timeout(budget):
            result = await Runner.run(
                agent, "What is SQL?", max_turns=3, run_config=run_config()
            )
        print("OK:", result.final_output)
    except TimeoutError:
        print(f"OK: SDK run cancelled at deadline={budget}s")


if __name__ == "__main__":
    asyncio.run(main())
