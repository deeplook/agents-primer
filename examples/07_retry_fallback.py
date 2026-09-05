"""Take a fallback edge when a bounded retry loop cannot recover."""

from _workflow import run_bounded


def main() -> None:
    try:
        run_bounded(lambda _attempt: False, limit=2)
    except RuntimeError:
        result = "fallback: create a human-support ticket"
        attempts = 2
    else:
        result = "unexpected success"
        attempts = 0
    print(f"OK: {result} after_attempts={attempts}")


if __name__ == "__main__":
    main()
