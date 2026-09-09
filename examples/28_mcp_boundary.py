"""Connect the SDK to a real local MCP server with a tool allowlist and approval."""

import asyncio
import sys
from pathlib import Path

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.mcp import MCPServerStdio, create_static_tool_filter
from agents.testing import assistant_message, function_call


async def main() -> None:
    async with MCPServerStdio(
        params={
            "command": sys.executable,
            "args": [str(Path(__file__).with_name("_mcp_server.py"))],
        },
        tool_filter=create_static_tool_filter(allowed_tool_names=["read_document"]),
        require_approval="always",
    ) as server:
        visible = [tool.name for tool in await server.list_tools()]
        assert visible == ["read_document"]
        agent = Agent(
            name="Research",
            instructions="Read the document using the MCP tool.",
            mcp_servers=[server],
            model=demo_model(
                [function_call("read_document", {}, call_id="mcp-1")],
                [assistant_message("Duplicates qualify for review.")],
            ),
        )
        paused = await Runner.run(
            agent, "Read the refund policy.", max_turns=3, run_config=run_config()
        )
        if not paused.interruptions:
            raise RuntimeError("expected MCP approval")
        state = paused.to_state()
        for item in paused.interruptions:
            state.approve(item)  # Demo decision for the known local read-only tool.
        result = await Runner.run(agent, state, run_config=run_config())
        outputs = [
            item.output
            for item in result.new_items
            if item.type == "tool_call_output_item"
        ]
        assert outputs, "MCP tool must execute after approval"
        print(
            f"OK: visible={visible} MCP outputs={outputs} reply={result.final_output}"
        )


if __name__ == "__main__":
    asyncio.run(main())
