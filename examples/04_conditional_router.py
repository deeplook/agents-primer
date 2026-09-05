"""Route a request deterministically to one specialist agent."""

import asyncio

from _shared import MODEL, key_or_skip
from _workflow import classify_request


async def main() -> None:
    if not key_or_skip():
        return
    from agents import Agent, Runner

    billing = Agent(
        name="Billing specialist",
        instructions="Answer billing questions in one concise sentence.",
        model=MODEL,
    )
    technical = Agent(
        name="Technical specialist",
        instructions="Answer technical questions in one concise sentence.",
        model=MODEL,
    )
    general = Agent(
        name="General specialist",
        instructions="Answer general questions in one concise sentence.",
        model=MODEL,
    )
    request = "My invoice needs a refund."
    specialists = {
        "billing": billing,
        "technical": technical,
        "general": general,
    }
    route = classify_request(request)
    result = await Runner.run(specialists[route], request)
    print(f"OK: route={route} output={result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
