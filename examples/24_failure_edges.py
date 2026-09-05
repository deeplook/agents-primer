"""Route predictable failures to a recovery node instead of raising blindly."""


def lookup_account(account_id: str) -> str:
    if account_id == "missing":
        raise LookupError("account unavailable")
    return "active"


def main() -> None:
    try:
        result = lookup_account("missing")
        edge = "continue"
    except LookupError:
        result = "ask user for account details"
        edge = "recovery"
    print(f"OK: edge={edge} result={result}")


if __name__ == "__main__":
    main()
