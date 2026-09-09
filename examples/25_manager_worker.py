"""The manager calls an SDK worker twice, then owns the final typed decision."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message, function_call
from pydantic import BaseModel


class Decision(BaseModel):
    evidence: str
    next_step: str


async def manage() -> tuple[str, Decision]:
    worker = Agent(
        name="Ledger worker",
        instructions="First establish the order ID; order 42 has two identical charges.",
        model=demo_model(
            [assistant_message("Need the order ID before checking.")],
            [assistant_message("Order 42 has two identical charges.")],
        ),
    )
    manager = Agent(
        name="Support manager",
        instructions="Ask check_ledger to verify duplicates. Supply order 42 if asked. "
        "Then propose human review; never claim money was refunded.",
        tools=[
            worker.as_tool(
                tool_name="check_ledger",
                tool_description="Check billing evidence.",
                max_turns=3,
            )
        ],
        output_type=Decision,
        model=demo_model(
            [
                function_call(
                    "check_ledger",
                    {"input": "Check for duplicates."},
                    call_id="worker-1",
                )
            ],
            [
                function_call(
                    "check_ledger", {"input": "The order ID is 42."}, call_id="worker-2"
                )
            ],
            [
                assistant_message(
                    '{"evidence":"Order 42 charged twice","next_step":"human review"}'
                )
            ],
        ),
    )
    result = await Runner.run(
        manager,
        "Review my duplicate charge for order 42.",
        max_turns=4,
        run_config=run_config(),
    )
    decision = result.final_output_as(Decision)
    print(f"OK: owner={result.last_agent.name} decision={decision.model_dump_json()}")
    return result.last_agent.name, decision


if __name__ == "__main__":
    asyncio.run(manage())
