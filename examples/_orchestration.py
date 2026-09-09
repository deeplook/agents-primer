"""Share the model boundary only; each lesson owns its orchestration."""

import json

from _shared import demo_model, run_config
from agents import Agent, Runner
from agents.testing import assistant_message
from pydantic import BaseModel


async def ask[Output: BaseModel](
    name: str,
    instructions: str,
    prompt: str,
    schema: type[Output],
    scripted: dict[str, object],
) -> Output:
    agent = Agent(
        name=name,
        instructions=instructions,
        model=demo_model([assistant_message(json.dumps(scripted))]),
        output_type=schema,
    )
    run = await Runner.run(agent, prompt, max_turns=3, run_config=run_config())
    result = schema.model_validate(run.final_output)
    print(f"{name}: {result.model_dump_json()}")
    return result


class Task(BaseModel):
    id: str
    action: str
    depends_on: list[str] = []


class Plan(BaseModel):
    tasks: list[Task]

    def validate_steps(self, allowed: set[str]) -> None:
        ids = [task.id for task in self.tasks]
        if not ids or len(ids) != len(set(ids)):
            raise ValueError("plan needs unique task IDs and at least one task")
        done: set[str] = set()
        for task in self.tasks:
            if task.action not in allowed or not set(task.depends_on) <= set(ids):
                raise ValueError("unknown action or dependency")
        while len(done) < len(ids):
            ready = {t.id for t in self.tasks if set(t.depends_on) <= done} - done
            if not ready:
                raise ValueError("cyclic dependencies")
            done.update(ready)
