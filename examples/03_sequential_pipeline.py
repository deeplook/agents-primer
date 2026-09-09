"""Feed a typed classifier result into a second SDK agent; Python owns sequencing."""

import asyncio
from typing import Literal

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message
from pydantic import BaseModel


class Route(BaseModel):
    team: Literal["billing", "technical", "general"]


async def main() -> None:
    classifier = Agent(
        name="Classifier",
        instructions="Choose the support team.",
        output_type=Route,
        model=demo_model([assistant_message('{"team":"billing"}')]),
    )
    classified = await Runner.run(
        classifier,
        "My invoice was charged twice.",
        run_config=run_config(),
        max_turns=3,
    )
    route = classified.final_output_as(Route)
    writer = Agent(
        name="Writer",
        instructions="Draft a brief assignment notice.",
        model=demo_model([assistant_message("Assigned to billing support.")]),
    )
    reply = await Runner.run(
        writer, f"Chosen team: {route.team}", run_config=run_config(), max_turns=3
    )
    print(f"OK: team={route.team} reply={reply.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
