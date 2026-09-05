"""Give an agent a typed Python function tool."""

import asyncio

from _shared import MODEL, key_or_skip


async def main() -> None:
    if not key_or_skip():
        return
    from agents import Agent, Runner, function_tool

    # @function_tool turns this typed Python function into a tool the agent can call.
    @function_tool
    def lookup_priority(customer: str) -> str:
        """Return the support priority for a customer."""
        return {"Ada": "high", "Bea": "normal"}.get(customer, "normal")

    agent = Agent(
        name="Support triage",
        instructions="Use lookup_priority when a customer is named.",
        model=MODEL,
        tools=[lookup_priority],
    )
    result = await Runner.run(agent, "What priority should Ada receive?")
    print("OK:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
