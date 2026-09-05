"""Convert a tool error into scoped context for the recovery edge."""


def recover(error: dict[str, str]) -> dict[str, object]:
    if error["code"] == "not_found":
        next_action = "ask for account ID"
    elif error["code"] == "timeout":
        next_action = "retry lookup"
    else:
        next_action = "escalate to human"
    return {"previous_error": error, "next_action": next_action}


def main() -> None:
    missing = recover({"tool": "lookup_account", "code": "not_found"})
    timeout = recover({"tool": "lookup_account", "code": "timeout"})
    print(f"OK: not_found={missing['next_action']} timeout={timeout['next_action']}")


if __name__ == "__main__":
    main()
