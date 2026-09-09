"""Python schedules ready tasks in waves; agents receive parent outputs.

Validate the graph first. A failed wave stops downstream execution.
Offline by default; --live runs each node through the SDK.
"""

import asyncio

from _orchestration import Plan, Task, ask
from pydantic import BaseModel


class Finding(BaseModel):
    text: str


async def execute(task: Task, inputs: dict[str, str]) -> str:
    result = await ask(
        task.id,
        "Perform the named review using supplied facts and parent findings.",
        f"Action: {task.action}. Facts: order 42 charged twice. Parents: {inputs}",
        Finding,
        {"text": f"{task.action}: reviewed using {sorted(inputs)}"},
    )
    return result.text


async def schedule(plan: Plan) -> dict[str, str]:
    plan.validate_steps({"read_invoice", "check_policy", "summarize"})
    results: dict[str, str] = {}
    while len(results) < len(plan.tasks):
        ready = [
            t
            for t in plan.tasks
            if t.id not in results and set(t.depends_on) <= results.keys()
        ]
        print(f"ready: {[t.id for t in ready]}")
        async with asyncio.TaskGroup() as group:
            running = [
                group.create_task(
                    execute(
                        task,
                        {key: results[key] for key in task.depends_on},
                    )
                )
                for task in ready
            ]
        results.update(
            (task.id, run.result()) for task, run in zip(ready, running, strict=True)
        )
    return results


async def main() -> None:
    plan = Plan(
        tasks=[
            Task(id="invoice", action="read_invoice"),
            Task(id="policy", action="check_policy"),
            Task(id="reply", action="summarize", depends_on=["invoice", "policy"]),
        ]
    )
    print(f"OK: results={await schedule(plan)}")


if __name__ == "__main__":
    asyncio.run(main())
