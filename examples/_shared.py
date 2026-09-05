"""Shared configuration for live Agents SDK examples."""

import os

MODEL = os.environ.get("OPENAI_AGENT_MODEL", "gpt-5-mini")


def key_or_skip() -> bool:
    if not os.environ.get("OPENAI_API_KEY"):
        print("SKIP: set OPENAI_API_KEY to run this Agents SDK example")
        return False
    return True
