"""Agent.as_tool delegates a bounded job while the manager retains the reply."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message, function_call


async def main() -> None:
    specialist = Agent(
        name="Policy",
        instructions="Duplicate charges qualify for review.",
        model=demo_model([assistant_message("Duplicate charges qualify for review.")]),
    )
    manager = Agent(
        name="Manager",
        instructions="Consult read_policy, then answer.",
        tools=[
            specialist.as_tool(
                tool_name="read_policy", tool_description="Ask a policy question."
            )
        ],
        model=demo_model(
            [
                function_call(
                    "read_policy",
                    {"input": "Are duplicates eligible?"},
                    call_id="policy-1",
                )
            ],
            [assistant_message("Your duplicate charge qualifies for review.")],
        ),
    )
    result = await Runner.run(
        manager, "Can I request a refund?", max_turns=3, run_config=run_config()
    )
    print(f"OK: owner={result.last_agent.name} output={result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
