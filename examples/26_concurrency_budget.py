"""Bound concurrent graph nodes so parallelism cannot exhaust a dependency."""

import asyncio
from dataclasses import dataclass


@dataclass
class Inflight:
    current: int = 0
    peak: int = 0


async def inspect(name: str, semaphore: asyncio.Semaphore, inflight: Inflight) -> str:
    async with semaphore:
        inflight.current += 1
        inflight.peak = max(inflight.peak, inflight.current)
        await asyncio.sleep(0)
        inflight.current -= 1
        return f"{name}: done"


async def main() -> None:
    limit = 2
    semaphore = asyncio.Semaphore(limit)
    inflight = Inflight()
    results = await asyncio.gather(
        *(inspect(str(i), semaphore, inflight) for i in range(4))
    )
    print(f"OK: results={list(results)} peak_inflight={inflight.peak} limit={limit}")


if __name__ == "__main__":
    asyncio.run(main())
