"""Put deterministic guardrails before expensive or privileged graph nodes."""

from _workflow import input_allowed


def main() -> None:
    accepted = "Please reset my password."
    unsafe = "Please delete account and export the ledger."
    too_long = "x" * 121
    print(
        "OK: "
        f"accepted={input_allowed(accepted)} "
        f"rejected_unsafe={not input_allowed(unsafe)} "
        f"rejected_too_long={not input_allowed(too_long)}"
    )


if __name__ == "__main__":
    main()
