"""Serialize an approval boundary rather than letting a workflow act silently."""


def gate(action: str, *, approved: bool) -> str:
    if not approved:
        return f"paused before {action}"
    return f"executed {action}"


def main() -> None:
    action = "issue a refund"
    print(
        f"OK: unapproved={gate(action, approved=False)} approved={gate(action, approved=True)}"
    )


if __name__ == "__main__":
    main()
