"""Keep workflow state explicit so each graph node has clear inputs and outputs."""

from _workflow import WorkflowState, classify_request


def intake(state: WorkflowState) -> None:
    state.route = classify_request(state.request)
    state.notes.append(f"intake classified as {state.route}")


def specialist(state: WorkflowState) -> None:
    if state.route is None:
        raise RuntimeError("specialist node requires state.route")
    state.notes.append(f"{state.route} node received request")


def main() -> None:
    state = WorkflowState(request="The app shows an error.")
    intake(state)
    specialist(state)
    print(f"OK: state={state}")


if __name__ == "__main__":
    main()
