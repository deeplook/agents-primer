"""An SDK tool guardrail blocks external action when context marks risky data access.

This teaching policy assumes trusted application labels; it is not an injection detector.
"""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner, function_tool
from agents.testing import assistant_message, function_call
from agents.tool_guardrails import (
    ToolGuardrailFunctionOutput,
    ToolInputGuardrailData,
    tool_input_guardrail,
)


@tool_input_guardrail
def boundary(data: ToolInputGuardrailData) -> ToolGuardrailFunctionOutput:
    flags = data.context.context
    if flags["untrusted_input"] and flags["sensitive_data"]:
        return ToolGuardrailFunctionOutput.reject_content(
            "External action blocked; request human review."
        )
    return ToolGuardrailFunctionOutput.allow()


async def main() -> None:
    effects: list[str] = []

    @function_tool(tool_input_guardrails=[boundary])
    def send_message() -> str:
        """Record a simulated outgoing message."""
        effects.append("sent")
        return "Simulated message sent."

    agent = Agent(
        name="Assistant",
        instructions="Call send_message and respect any rejection.",
        tools=[send_message],
        model=demo_model(
            [function_call("send_message", {}, call_id="send-1")],
            [assistant_message("External action blocked; human review needed.")],
        ),
    )
    result = await Runner.run(
        agent,
        "Send the document.",
        context={"untrusted_input": True, "sensitive_data": True},
        max_turns=3,
        run_config=run_config(),
    )
    assert not effects
    print(f"OK: effects={effects} output={result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
