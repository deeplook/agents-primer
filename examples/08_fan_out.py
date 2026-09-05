"""Fan out independent specialist work concurrently, then keep every result."""

import asyncio


async def inspect(name: str) -> str:
    await asyncio.sleep(0)
    return f"{name}: checked"


async def main() -> None:
    specialists = ("logs", "billing", "status")
    results = await asyncio.gather(*(inspect(name) for name in specialists))
    print(f"OK: kept={list(results)} count={len(results)}")


if __name__ == "__main__":
    asyncio.run(main())
