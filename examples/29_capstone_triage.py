"""Run a small bounded support-triage graph end to end without a model call."""

from _workflow import (
    WorkflowState,
    classify_request,
    input_allowed,
    output_deliverable,
)


def handle(request: str) -> str:
    if not input_allowed(request):
        return "rejected:input"
    state = WorkflowState(request=request)
    state.route = classify_request(state.request)
    if state.route == "billing":
        state.notes.append("paused for refund approval")
        return "paused:refund_approval"
    reply = f"Answer: assigned {state.route} support."
    if not output_deliverable(reply):
        return "rejected:output"
    state.notes.extend([f"assigned {state.route}", "synthesized reply"])
    return f"resolved:{state.route}"


def main() -> None:
    outcomes = [
        handle("The app shows an error after sign-in."),
        handle("Please delete account immediately."),
        handle("My invoice needs a refund."),
    ]
    print(f"OK: outcomes={outcomes}")


if __name__ == "__main__":
    main()
