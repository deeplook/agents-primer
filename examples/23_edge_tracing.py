"""Record graph edges so a workflow can be debugged after it runs."""

from _workflow import classify_request


def walk(request: str) -> list[tuple[str, str]]:
    route = classify_request(request)
    successors: dict[str, str | None] = {
        "intake": "route",
        "route": route,
        "billing": "synthesize",
        "technical": "synthesize",
        "general": "synthesize",
        "synthesize": None,
    }
    trace: list[tuple[str, str]] = []
    node = "intake"
    while successors[node]:
        nxt = successors[node]
        assert nxt is not None
        trace.append((node, nxt))
        node = nxt
    return trace


def main() -> None:
    trace = walk("The app shows an error.")
    print(f"OK: trace={trace}")


if __name__ == "__main__":
    main()
