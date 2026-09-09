"""An SDK input guardrail blocks a run before the model is called."""

import asyncio
from typing import Any

from _shared import demo_model, run_config
from _workflow import input_allowed
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
from agents.testing import assistant_message


@input_guardrail(run_in_parallel=False)
def scope(
    ctx: RunContextWrapper[None],
    agent: Agent[Any],
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    # A teaching policy, not a general-purpose safety classifier.
    allowed = isinstance(input, str) and input_allowed(input)
    return GuardrailFunctionOutput(
        output_info={"allowed": allowed}, tripwire_triggered=not allowed
    )


async def main() -> None:
    for request in ["Please reset my password.", "Please delete account now."]:
        agent = Agent(
            name="Support",
            input_guardrails=[scope],
            model=demo_model([assistant_message("Answer: Use password reset.")]),
        )
        try:
            result = await Runner.run(
                agent, request, max_turns=3, run_config=run_config()
            )
            print("OK: accepted", result.final_output)
        except InputGuardrailTripwireTriggered:
            print("OK: blocked before model call")


if __name__ == "__main__":
    asyncio.run(main())
