"""Cancel a running SDK agent while it awaits a tool; verify tool cleanup."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner, function_tool
from agents.testing import function_call


async def main() -> None:
    started, cleaned = asyncio.Event(), asyncio.Event()

    @function_tool
    async def slow_lookup() -> str:
        """Wait for an unavailable dependency (injected in both modes)."""
        started.set()
        try:
            await asyncio.Event().wait()
        finally:
            cleaned.set()
        return "unreachable"

    agent = Agent(
        name="Lookup",
        instructions="Call slow_lookup.",
        tools=[slow_lookup],
        model=demo_model([function_call("slow_lookup", {}, call_id="slow-1")]),
    )
    task = asyncio.create_task(
        Runner.run(agent, "Look up order 42.", run_config=run_config(), max_turns=3)
    )
    try:
        await asyncio.wait_for(started.wait(), timeout=30)
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    assert cleaned.is_set()
    print("OK: SDK run cancelled; tool finally block completed")


if __name__ == "__main__":
    asyncio.run(main())
