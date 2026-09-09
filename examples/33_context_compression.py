"""An SDK summarizer produces typed carry-forward context for the next agent."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message
from pydantic import BaseModel


class Summary(BaseModel):
    facts: list[str]
    pending: str


async def main() -> None:
    summarizer = Agent(
        name="Summarizer",
        instructions="Preserve verified facts and unresolved work; do not infer approval.",
        output_type=Summary,
        model=demo_model(
            [
                assistant_message(
                    '{"facts":["account verified","duplicate charge found"],"pending":"human approval"}'
                )
            ]
        ),
    )
    result = await Runner.run(
        summarizer,
        "Opened ticket. Verified account. Checked invoice. Found duplicate charge. Approval pending.",
        max_turns=3,
        run_config=run_config(),
    )
    summary = result.final_output_as(Summary)
    responder = Agent(
        name="Responder",
        instructions="Explain the next step using only the summary.",
        model=demo_model(
            [assistant_message("The duplicate charge awaits human approval.")]
        ),
    )
    reply = await Runner.run(
        responder, summary.model_dump_json(), max_turns=3, run_config=run_config()
    )
    print(f"OK: carried={summary.model_dump_json()} reply={reply.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
