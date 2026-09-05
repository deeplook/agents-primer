"""Every agentic loop needs an explicit termination budget."""

from _workflow import run_bounded


def main() -> None:
    attempts = run_bounded(lambda attempt: attempt == 3, limit=4)
    print(f"OK: completed_on_attempt={attempts}")


if __name__ == "__main__":
    main()
