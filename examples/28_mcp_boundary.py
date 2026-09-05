"""Model an MCP call as a privileged edge requiring trust and approval."""


def call_mcp(edge: dict[str, object], *, tool: str, approved: bool) -> str:
    allowed = edge["allowed_tools"]
    assert isinstance(allowed, list)
    if tool not in allowed:
        return f"denied: {tool} not on allowlist"
    if edge["requires_approval"] and not approved:
        return f"paused: approval required for {edge['to']}"
    return f"called {edge['to']}.{tool}"


def main() -> None:
    edge = {
        "from": "research_agent",
        "to": "remote_mcp",
        "allowed_tools": ["read_document"],
        "requires_approval": True,
    }
    print(
        "OK: "
        f"blocked={call_mcp(edge, tool='read_document', approved=False)} "
        f"allowed={call_mcp(edge, tool='read_document', approved=True)} "
        f"overreach={call_mcp(edge, tool='delete_file', approved=True)}"
    )


if __name__ == "__main__":
    main()
