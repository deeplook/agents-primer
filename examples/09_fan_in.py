"""Merge typed SDK results in Python; the merge policy decides whether to escalate."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message
from pydantic import BaseModel


class Finding(BaseModel):
    source: str
    blocked: bool
    evidence: str


async def main() -> None:
    findings = []
    for source, blocked in [("ledger", False), ("policy", True)]:
        fixture = Finding(
            source=source,
            blocked=blocked,
            evidence="Policy service unavailable."
            if blocked
            else "Duplicate verified.",
        )
        agent = Agent(
            name=source,
            instructions="Report the supplied evidence; mark missing evidence blocked.",
            output_type=Finding,
            model=demo_model([assistant_message(fixture.model_dump_json())]),
        )
        result = await Runner.run(
            agent, fixture.evidence, max_turns=3, run_config=run_config()
        )
        findings.append(result.final_output_as(Finding))
    decision = "escalate" if any(f.blocked for f in findings) else "continue"
    print(f"OK: decision={decision} sources={[f.source for f in findings]}")


if __name__ == "__main__":
    asyncio.run(main())
