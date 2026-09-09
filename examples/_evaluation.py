"""Evaluate typed SDK routing; offline fixtures exercise plumbing, not model quality."""

from typing import Literal

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message
from pydantic import BaseModel


class Route(BaseModel):
    team: Literal["billing", "technical", "general"]


CASES = [
    ("Refund my invoice.", "billing"),
    ("The app crashes.", "technical"),
    ("What are your hours?", "general"),
]


async def evaluate() -> list[tuple[str, str, str, int]]:
    records: list[tuple[str, str, str, int]] = []
    for request, expected in CASES:
        agent = Agent(
            name="Router",
            instructions="Choose billing, technical, or general.",
            output_type=Route,
            model=demo_model([assistant_message(f'{{"team":"{expected}"}}')]),
        )
        result = await Runner.run(agent, request, max_turns=3, run_config=run_config())
        records.append(
            (
                request,
                expected,
                result.final_output_as(Route).team,
                len(result.raw_responses),
            )
        )
    return records
