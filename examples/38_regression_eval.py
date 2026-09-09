"""Assert routing outcomes from SDK runs; --live evaluates actual model behavior."""

import asyncio

from _evaluation import evaluate


async def main() -> None:
    records = await evaluate()
    failures = [
        f"{request}: expected {expected}, got {actual}"
        for request, expected, actual, _ in records
        if expected != actual
    ]
    if failures:
        raise AssertionError("\n".join(failures))
    print(f"OK: SDK routing regression={len(records)}/{len(records)}")


if __name__ == "__main__":
    asyncio.run(main())
