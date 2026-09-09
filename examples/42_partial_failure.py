"""Keep successful findings when a specialist misses its deadline.

Python requires ledger evidence; optional policy failure yields a partial answer.
The policy deadline is deliberately tiny; offline its model wait never completes.
"""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import ModelCall, ModelStep, assistant_message
from pydantic import BaseModel


class Finding(BaseModel):
    evidence: str


async def inspect(name: str, unavailable: bool) -> Finding:
    async def stalled(call: ModelCall) -> ModelStep:
        await asyncio.Event().wait()
        raise AssertionError("unreachable")

    step = (
        ModelStep.respond(stalled)
        if unavailable
        else ModelStep(
            output=[assistant_message('{"evidence":"Duplicate charge verified."}')]
        )
    )
    agent = Agent(
        name=name,
        instructions="Report only supplied evidence.",
        output_type=Finding,
        model=demo_model(step),
    )
    async with asyncio.timeout(0.01 if unavailable else 30):
        result = await Runner.run(
            agent, "Order 42 has two charges.", max_turns=3, run_config=run_config()
        )
        return result.final_output_as(Finding)


async def collect(required: str = "ledger") -> tuple[dict[str, Finding], str]:
    names = ["ledger", "policy"]
    outcomes = await asyncio.gather(
        inspect("ledger", False),
        inspect("policy", True),
        return_exceptions=True,
    )
    findings = {}
    for name, outcome in zip(names, outcomes, strict=True):
        if isinstance(outcome, TimeoutError):
            print(f"{name}: unavailable; preserve other findings")
        elif isinstance(outcome, BaseException):
            raise outcome
        else:
            findings[name] = outcome
    status = "complete" if len(findings) == len(names) else "partial: human review"
    if required not in findings:
        status = "blocked: missing evidence"
    return findings, status


async def main() -> None:
    findings, status = await collect()
    print(f"OK: kept={list(findings)} status={status}")


if __name__ == "__main__":
    asyncio.run(main())
