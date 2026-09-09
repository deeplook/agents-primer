"""The SDK proposes typed transitions; Python enforces the workflow state machine."""

import asyncio
from typing import Literal

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message
from pydantic import BaseModel


class Transition(BaseModel):
    next_state: Literal["review", "done"]
    reason: str


async def main() -> None:
    legal = {"new": {"review"}, "review": {"done"}}
    state = "new"
    agent = Agent(
        name="Coordinator",
        instructions="Move new -> review -> done, one step at a time.",
        output_type=Transition,
        model=demo_model(
            [assistant_message('{"next_state":"review","reason":"needs review"}')],
            [assistant_message('{"next_state":"done","reason":"review complete"}')],
        ),
    )
    for _ in range(2):
        result = await Runner.run(
            agent, f"Current state: {state}", max_turns=3, run_config=run_config()
        )
        proposed = result.final_output_as(Transition)
        if proposed.next_state not in legal.get(state, set()):
            raise ValueError(f"illegal transition {state} -> {proposed.next_state}")
        print(f"{state} -> {proposed.next_state}: {proposed.reason}")
        state = proposed.next_state
    assert state == "done"
    print("OK: reached terminal state")


if __name__ == "__main__":
    asyncio.run(main())
