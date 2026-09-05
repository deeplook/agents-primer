"""Run a tiny deterministic evaluation suite over workflow behavior."""

from _workflow import classify_request, input_allowed, output_deliverable


def main() -> None:
    routing = [
        ("Please refund my invoice", "billing"),
        ("The app shows an error", "technical"),
        ("What are your hours?", "general"),
    ]
    routing_passed = sum(
        classify_request(request) == expected for request, expected in routing
    )
    guardrails_passed = sum(
        [
            input_allowed("Please reset my password."),
            not input_allowed("Please delete account now."),
            output_deliverable("Answer: Your refund is being reviewed."),
            not output_deliverable("Answer: internal account 12 is past due."),
        ]
    )
    print(
        f"OK: routing={routing_passed}/{len(routing)} guardrails={guardrails_passed}/4"
    )


if __name__ == "__main__":
    main()
