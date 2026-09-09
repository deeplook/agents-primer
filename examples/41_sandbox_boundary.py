"""Configure SDK hosted code execution instead of pretending a path check is a sandbox.

Offline inspects configuration only. --live runs code in the provider's container
and incurs model plus container charges. No host shell tool is exposed.
"""

import asyncio

from _shared import demo_model, live, run_config
from agents import Agent, CodeInterpreterTool, Runner


async def main() -> None:
    interpreter = CodeInterpreterTool(
        tool_config={
            "type": "code_interpreter",
            "container": {"type": "auto"},
        }
    )
    agent = Agent(
        name="Calculator",
        instructions="Use code interpreter to calculate sum(range(100)).",
        tools=[interpreter],
        model=demo_model(),
    )
    if not live():
        print(
            f"OK: SDK hosted tool configured={interpreter.tool_config}; no code executed"
        )
        return
    result = await Runner.run(
        agent, "Calculate the sum.", max_turns=3, run_config=run_config()
    )
    print("OK:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
