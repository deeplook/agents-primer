"""SDK specialists return conflicting typed claims; Python chooses by authority."""

import asyncio

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message
from pydantic import BaseModel


class Claim(BaseModel):
    amount: int
    evidence: str


async def main() -> None:
    findings: dict[str, Claim] = {}
    for source, amount in [("ledger", 20), ("email", 25)]:
        fixture = Claim(amount=amount, evidence=f"{source} lists {amount} EUR.")
        agent = Agent(
            name=source,
            instructions="Extract the amount from the provided record.",
            output_type=Claim,
            model=demo_model([assistant_message(fixture.model_dump_json())]),
        )
        result = await Runner.run(
            agent, fixture.evidence, max_turns=3, run_config=run_config()
        )
        findings[source] = result.final_output_as(
            Claim
        )  # Source identity comes from Python.
    chosen = findings["ledger"]
    disagreement = len({claim.amount for claim in findings.values()}) > 1
    print(
        f"OK: conflict={disagreement} chosen={chosen.amount} reason=ledger_is_authoritative"
    )


if __name__ == "__main__":
    asyncio.run(main())
