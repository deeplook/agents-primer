"""Checkpoint serializable state so an interrupted graph can resume safely."""

import json
from pathlib import Path


def remaining(order: list[str], completed: list[str], current: str) -> list[str]:
    start = order.index(current)
    return completed + order[start:]


def main() -> None:
    checkpoint = Path("out/checkpoint.json")
    checkpoint.parent.mkdir(exist_ok=True)
    interrupted = {
        "node": "technical",
        "request_id": "demo-1",
        "completed": ["intake", "route"],
    }
    checkpoint.write_text(json.dumps(interrupted))
    saved = json.loads(checkpoint.read_text())
    trail = remaining(
        ["intake", "route", "technical", "synthesize"],
        saved["completed"],
        saved["node"],
    )
    print(
        f"OK: resume_at={saved['node']} trail={trail} skipped_replay={saved['completed']}"
    )


if __name__ == "__main__":
    main()
