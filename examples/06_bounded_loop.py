"""Runner.max_turns stops a model/tool loop with MaxTurnsExceeded."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, MaxTurnsExceeded, Runner, function_tool
from agents.testing import function_call


@function_tool
def inspect_again() -> str:
    """Return another inconclusive observation."""
    return "Still inconclusive."


async def main() -> None:
    agent = Agent(
        name="Investigator",
        instructions="Keep calling inspect_again.",
        tools=[inspect_again],
        model=demo_model(
            *[
                [function_call("inspect_again", {}, call_id=f"inspect-{i}")]
                for i in range(3)
            ]
        ),
    )
    try:
        await Runner.run(agent, "Investigate.", max_turns=2, run_config=run_config())
    except MaxTurnsExceeded:
        print("OK: runner stopped after two model turns")
    else:
        print("OK: model finished before the turn limit")


if __name__ == "__main__":
    asyncio.run(main())
