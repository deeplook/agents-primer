"""Define measurable workflow success criteria rather than a vague 'good answer'."""

from _workflow import classify_request, tool_allowed


def main() -> None:
    routing_cases = [
        ("Please refund my invoice", "billing"),
        ("The app shows an error", "technical"),
        ("What are your hours?", "general"),
    ]
    routing_accuracy = sum(
        classify_request(request) == expected for request, expected in routing_cases
    ) / len(routing_cases)
    approval_bypass = (
        1.0 if tool_allowed("research_agent", "request_refund_approval") else 0.0
    )
    metrics = {
        "routing_accuracy": routing_accuracy,
        "approval_bypass": approval_bypass,
        "max_steps": 6,
    }
    print(f"OK: metrics={metrics}")


if __name__ == "__main__":
    main()
