"""Read-only local MCP fixture used by example 28; no credentials or network."""

from mcp.server import MCPServer

server = MCPServer("Primer policy")


@server.tool()
def read_document() -> str:
    """Read the public refund policy."""
    return "Duplicate charges qualify for human review."


@server.tool()
def unrelated_tool() -> str:
    """A harmless tool excluded by the client's allowlist."""
    return "Not part of the research capability."


if __name__ == "__main__":
    server.run(transport="stdio")
