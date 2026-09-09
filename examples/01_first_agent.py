"""Run a real Agent and Runner, with a scripted model unless --live is supplied."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message


async def main() -> None:
    agent = Agent(
        name="Tutor",
        instructions="Explain workflow graphs in one sentence.",
        model=demo_model([assistant_message("A graph connects tasks and decisions.")]),
    )
    result = await Runner.run(
        agent, "What is a workflow graph?", max_turns=3, run_config=run_config()
    )
    print("OK:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
