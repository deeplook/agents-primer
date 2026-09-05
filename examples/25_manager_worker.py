"""A manager can delegate bounded work while retaining final decision authority."""


def worker(question: str) -> str:
    return "issue refund immediately"


def manager(question: str) -> str:
    proposal = worker(question)
    if "refund" in proposal and "confirmed" not in question:
        return f"rejected worker proposal ({proposal}); request approval"
    return f"accepted: {proposal}"


def main() -> None:
    print(
        f"OK: tentative={manager('refund policy')} "
        f"confirmed={manager('confirmed duplicate charge')}"
    )


if __name__ == "__main__":
    main()
