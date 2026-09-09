"""A semaphore bounds concurrent SDK runs; finally releases in-flight accounting."""

import asyncio
from dataclasses import dataclass

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message


@dataclass
class Inflight:
    current: int = 0
    peak: int = 0


async def inspect(name: str, semaphore: asyncio.Semaphore, inflight: Inflight) -> str:
    async with semaphore:
        inflight.current += 1
        inflight.peak = max(inflight.peak, inflight.current)
        try:
            agent = Agent(
                name=name,
                instructions="Return one brief finding.",
                model=demo_model([assistant_message(f"{name}: checked")]),
            )
            result = await Runner.run(
                agent, "Inspect order 42.", max_turns=3, run_config=run_config()
            )
            return str(result.final_output)
        finally:
            inflight.current -= 1


async def main() -> None:
    limit, inflight = 2, Inflight()
    semaphore = asyncio.Semaphore(limit)
    results = await asyncio.gather(
        *(inspect(str(i), semaphore, inflight) for i in range(4))
    )
    assert inflight.peak <= limit and inflight.current == 0
    print(f"OK: results={results} peak_inflight={inflight.peak} limit={limit}")


if __name__ == "__main__":
    asyncio.run(main())
