"""Use named states to make an agent workflow's legal transitions visible."""

TRANSITIONS = {"new": "routed", "routed": "resolved", "resolved": "done"}


def can_go(src: str, dst: str) -> bool:
    return TRANSITIONS.get(src) == dst


def main() -> None:
    state = "new"
    history = [state]
    while state != "done":
        state = TRANSITIONS[state]
        history.append(state)
    print(f"OK: {' -> '.join(history)} illegal_new_to_done={can_go('new', 'done')}")


if __name__ == "__main__":
    main()
