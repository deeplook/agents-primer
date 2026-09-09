"""Use typed SDK handoff arguments and explicitly filter the specialist's history."""

import asyncio
from dataclasses import replace
from typing import Any

from _shared import demo_model, run_config
from agents import Agent, HandoffInputData, RunContextWrapper, Runner, handoff
from agents.testing import assistant_message, function_call
from pydantic import BaseModel


class Brief(BaseModel):
    issue: str


def receive(ctx: RunContextWrapper[dict[str, str]], brief: Brief) -> None:
    ctx.context["issue"] = brief.issue


def scoped_history(data: HandoffInputData) -> HandoffInputData:
    # Keep SDK call/output items, but replace the original conversation history.
    return replace(
        data, input_history="Customer needs refund guidance.", pre_handoff_items=()
    )


async def main() -> None:
    billing: Agent[Any] = Agent(
        name="Billing",
        instructions="Answer the scoped billing request.",
        model=demo_model([assistant_message("Please provide the invoice number.")]),
    )
    triage: Agent[Any] = Agent(
        name="Triage",
        instructions="Transfer to billing with a brief issue.",
        handoffs=[
            handoff(
                billing,
                input_type=Brief,
                on_handoff=receive,
                input_filter=scoped_history,
            )
        ],
        model=demo_model(
            [
                function_call(
                    "transfer_to_billing", {"issue": "refund"}, call_id="brief-1"
                )
            ]
        ),
    )
    context: dict[str, str] = {}
    result = await Runner.run(
        triage,
        "Refund question. Internal note: demo-only.",
        context=context,
        max_turns=3,
        run_config=run_config(),
    )
    print(f"OK: owner={result.last_agent.name} handoff_metadata={context}")


if __name__ == "__main__":
    asyncio.run(main())
