"""Validate an output at the graph boundary before sending it to a user."""

from _workflow import output_deliverable


def main() -> None:
    safe = "Answer: Your refund is being reviewed."
    leak = "Answer: internal account 442 is past due."
    unprefixed = "Sure, we can do that."
    print(
        "OK: "
        f"accepted={output_deliverable(safe)} "
        f"rejected_leak={not output_deliverable(leak)} "
        f"rejected_shape={not output_deliverable(unprefixed)}"
    )


if __name__ == "__main__":
    main()
