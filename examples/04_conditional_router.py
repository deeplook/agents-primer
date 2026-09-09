"""Python selects an SDK agent deterministically; only that specialist runs."""

import asyncio

from _shared import demo_model, run_config
from _workflow import classify_request
from agents import Agent, Runner
from agents.testing import assistant_message


async def main() -> None:
    specialists = {
        name: Agent(
            name=name,
            instructions=f"Answer {name} questions briefly.",
            model=demo_model([assistant_message(f"Assigned to {name} support.")]),
        )
        for name in ("billing", "technical", "general")
    }
    request = "My invoice needs a refund."
    route = classify_request(request)
    result = await Runner.run(
        specialists[route], request, max_turns=3, run_config=run_config()
    )
    print(f"OK: route={route} output={result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
