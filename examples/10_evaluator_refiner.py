"""A writer revises from typed critique; Python caps rounds and detects stagnation.

Offline by default; --live uses the same loop with SDK calls.
"""

import asyncio

from _orchestration import ask
from pydantic import BaseModel, Field


class Draft(BaseModel):
    text: str


class Critique(BaseModel):
    accepted: bool
    score: int = Field(ge=0, le=10)
    issues: list[str]


async def revise(limit: int = 3) -> tuple[str, str]:
    if limit < 1:
        raise ValueError("limit must be positive")
    feedback = "Write a reply: duplicate charge verified; refund needs human approval."
    best, best_score, seen = "", -1, set()
    for round_number in range(limit):
        draft = await ask(
            "Writer",
            "Use facts and critique. Never claim a refund was issued.",
            feedback,
            Draft,
            {
                "text": "Refund issued."
                if round_number == 0
                else "Refund awaiting approval."
            },
        )
        if draft.text in seen:
            return best, "stalled"
        seen.add(draft.text)
        critique = await ask(
            "Reviewer",
            "Accept only a clear reply saying approval is still required.",
            draft.text,
            Critique,
            {
                "accepted": round_number > 0,
                "score": 3 if round_number == 0 else 9,
                "issues": ["State that human approval is required."]
                if round_number == 0
                else [],
            },
        )
        if critique.score > best_score:
            best, best_score = draft.text, critique.score
        if critique.accepted and not critique.issues:
            return draft.text, "accepted"
        feedback = f"Facts: refund requires approval.\nDraft: {draft.text}\n{critique.model_dump_json()}"
    return best, "budget_exhausted"  # Candidate for review, not an approved answer.


async def main() -> None:
    text, status = await revise()
    print(f"OK: status={status} candidate={text!r}")


if __name__ == "__main__":
    asyncio.run(main())
