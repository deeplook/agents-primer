"""Expose only the tools a graph node needs for its assigned responsibility."""

from _workflow import tool_allowed


def invoke(agent: str, tool: str) -> str:
    if not tool_allowed(agent, tool):
        return f"denied:{agent}:{tool}"
    return f"allowed:{agent}:{tool}"


def main() -> None:
    print(
        "OK: "
        f"research_search={invoke('research_agent', 'search_documents')} "
        f"research_refund={invoke('research_agent', 'request_refund_approval')} "
        f"refund_approval={invoke('refund_agent', 'request_refund_approval')}"
    )


if __name__ == "__main__":
    main()
