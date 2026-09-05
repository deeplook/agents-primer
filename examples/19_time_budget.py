"""Stop queued workflow steps when the remaining time budget is gone."""


def run_with_time_budget(
    steps: list[tuple[str, float]], budget: float
) -> tuple[list[str], str | None]:
    remaining = budget
    completed: list[str] = []
    for name, cost in steps:
        if cost > remaining:
            return completed, name
        remaining -= cost
        completed.append(name)
    return completed, None


def main() -> None:
    steps = [
        ("intake", 0.2),
        ("research", 0.4),
        ("draft", 0.4),
        ("send", 0.3),
    ]
    completed, stopped_before = run_with_time_budget(steps, budget=0.7)
    print(f"OK: completed={completed} stopped_before={stopped_before}")


if __name__ == "__main__":
    main()
