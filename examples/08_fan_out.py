"""Python runs two specialists concurrently; a synthesizer owns the final reply.

Offline by default; --live uses SDK calls with three turns per agent.
"""

import asyncio

from _orchestration import ask
from pydantic import BaseModel


class Finding(BaseModel):
    evidence: str


class Reply(BaseModel):
    text: str


async def investigate() -> Reply:
    jobs = [
        ("Ledger", "Check charges.", "Two charges share order 42."),
        (
            "Policy",
            "Check eligibility.",
            "Verified duplicates qualify for refund review.",
        ),
    ]
    findings = await asyncio.gather(
        *(
            ask(name, instructions, evidence, Finding, {"evidence": evidence})
            for name, instructions, evidence in jobs
        )
    )
    # Only validated specialist outputs cross into the synthesis step.
    brief = "\n".join(f.model_dump_json() for f in findings)
    return await ask(
        "Support",
        "Combine findings; propose next steps without issuing refunds.",
        brief,
        Reply,
        {"text": "The duplicate charge qualifies for refund review."},
    )


async def main() -> None:
    reply = await investigate()
    print(f"OK: specialists=2 reply={reply.text}")


if __name__ == "__main__":
    asyncio.run(main())
