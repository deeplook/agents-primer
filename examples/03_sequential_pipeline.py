"""Make the edges explicit when one workflow step feeds the next."""

from _workflow import classify_request


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def draft(route: str) -> str:
    return f"Answer: assigned to {route} support."


def main() -> None:
    raw = "  Please   refund my INVOICE  "
    normalized = normalize(raw)
    route = classify_request(normalized)
    result = draft(route)
    print(f"OK: {raw!r} -> {normalized!r} -> {route} -> {result}")


if __name__ == "__main__":
    main()
