"""An agent revises failed work; Python preserves completed IDs and actions.

One replan is allowed. --live enables the replanner; tools remain simulated.
"""

import asyncio

from _orchestration import Plan, Task, ask


def execute(action: str) -> str:
    if action == "lookup_policy":
        raise TimeoutError("policy service unavailable")
    return {
        "read_invoice": "Duplicate verified.",
        "queue_review": "Queued for human policy review.",
    }[action]


async def resolve() -> dict[str, str]:
    pending = Plan(
        tasks=[
            Task(id="invoice", action="read_invoice"),
            Task(id="policy", action="lookup_policy"),
        ]
    )
    results: dict[str, str] = {}
    completed_actions: set[str] = set()
    for revision in range(2):
        pending.validate_steps({"read_invoice", "lookup_policy", "queue_review"})
        if len({t.action for t in pending.tasks}) != len(pending.tasks):
            raise ValueError("replacement repeats an action")
        if any(
            t.id in results or t.action in completed_actions or t.depends_on
            for t in pending.tasks
        ):
            raise ValueError(
                "replacement must contain only independent unfinished work"
            )
        try:
            for task in pending.tasks:
                results[task.id] = execute(task.action)
                completed_actions.add(task.action)
                print(f"completed: {task.id}")
            return results
        except TimeoutError as error:
            if revision == 1:
                raise RuntimeError("replan budget exhausted") from error
            pending = await ask(
                "Replanner",
                "Replace remaining work with queue_review; never replay completed work.",
                f"Completed: {results}. Failed: {task.id}. Error: {error}",
                Plan,
                {"tasks": [{"id": "human", "action": "queue_review"}]},
            )
    raise AssertionError("unreachable")


async def main() -> None:
    print(f"OK: results={await resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
