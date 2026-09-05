"""Represent a plan as data, then execute only its approved steps."""


def execute(plan: list[dict[str, object]]) -> dict[str, list[str]]:
    executed = [str(item["step"]) for item in plan if item["approved"]]
    skipped = [str(item["step"]) for item in plan if not item["approved"]]
    return {"executed": executed, "skipped": skipped}


def main() -> None:
    plan = [
        {"step": "classify request", "approved": True},
        {"step": "look up account", "approved": True},
        {"step": "issue refund", "approved": False},
    ]
    result = execute(plan)
    print(f"OK: executed={result['executed']} skipped={result['skipped']}")


if __name__ == "__main__":
    main()
