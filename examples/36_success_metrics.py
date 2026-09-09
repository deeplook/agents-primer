"""Measure typed SDK results and actual model-turn counts over a small case set."""

import asyncio

from _evaluation import evaluate
from _shared import live


async def main() -> None:
    records = await evaluate()
    accuracy = sum(expected == actual for _, expected, actual, _ in records) / len(
        records
    )
    max_turns = max(turns for _, _, _, turns in records)
    print(
        f"OK: mode={'live' if live() else 'scripted'} "
        f"routing_accuracy={accuracy:.2f} max_model_turns={max_turns}"
    )


if __name__ == "__main__":
    asyncio.run(main())
