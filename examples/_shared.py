"""Choose the real model or the SDK's offline model double; never skip the runner."""

import os
import sys

from agents import Model, RunConfig
from agents.items import TResponseOutputItem
from agents.testing import ModelStep, ScriptedModel

MODEL = os.environ.get("OPENAI_AGENT_MODEL", "gpt-5-mini")


def live() -> bool:
    return "--live" in sys.argv


def demo_model(
    *steps: ModelStep | list[TResponseOutputItem] | Exception,
) -> Model | str:
    if live():
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("--live requires OPENAI_API_KEY")
        return MODEL
    return ScriptedModel(steps)


def run_config() -> RunConfig:
    # Even when a key is present, offline examples must not export traces.
    return RunConfig(tracing_disabled=not live())
