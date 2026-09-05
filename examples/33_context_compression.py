"""Carry a compact summary forward instead of every historical event."""


def compress(events: list[str]) -> dict[str, str]:
    last = events[-1]
    if "duplicate charge" in last:
        status, next_step = "duplicate charge found", "request approval"
    elif "verified" in last:
        status, next_step = "account verified", "continue"
    else:
        status, next_step = last, "investigate"
    return {
        "status": status,
        "next_step": next_step,
        "dropped_events": str(len(events) - 1),
    }


def main() -> None:
    events = [
        "opened ticket",
        "verified account",
        "checked invoice",
        "found duplicate charge",
    ]
    print(f"OK: events={len(events)} compressed={compress(events)}")


if __name__ == "__main__":
    main()
