"""An SDK output guardrail raises before an unacceptable final answer is returned."""

import asyncio
from typing import Any

from _shared import demo_model, run_config
from _workflow import output_deliverable
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)
from agents.testing import assistant_message


@output_guardrail
def delivery(
    ctx: RunContextWrapper[None], agent: Agent[Any], output: str
) -> GuardrailFunctionOutput:
    allowed = output_deliverable(output)
    return GuardrailFunctionOutput(
        output_info={"allowed": allowed}, tripwire_triggered=not allowed
    )


async def main() -> None:
    for text in [
        "Answer: Your refund is being reviewed.",
        "Answer: internal account 442.",
    ]:
        agent = Agent(
            name="Support",
            instructions="Repeat the supplied text exactly.",
            output_guardrails=[delivery],
            model=demo_model([assistant_message(text)]),
        )
        try:
            result = await Runner.run(agent, text, max_turns=3, run_config=run_config())
            print("OK: delivered", result.final_output)
        except OutputGuardrailTripwireTriggered:
            print("OK: output blocked by SDK")


if __name__ == "__main__":
    asyncio.run(main())
