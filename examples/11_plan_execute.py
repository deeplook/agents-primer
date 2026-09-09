"""An agent proposes a typed plan; Python validates it before executing any step.

Sequential plans only. --live enables the planner SDK call. Actions are simulated.
"""

import asyncio
from collections.abc import Callable

from _orchestration import Plan, ask

ACTIONS: dict[str, Callable[[], str]] = {
    "read_invoice": lambda: "Order 42 was charged twice.",
    "check_policy": lambda: "Duplicate charges qualify for approval review.",
    "request_approval": lambda: "Refund proposed; no money moved.",
}


def execute(plan: Plan) -> dict[str, str]:
    plan.validate_steps(set(ACTIONS))
    done: set[str] = set()
    for task in plan.tasks:
        if not set(task.depends_on) <= done:
            raise ValueError("sequential plan has a forward dependency")
        done.add(task.id)
    results = {}
    for task in plan.tasks:
        results[task.id] = ACTIONS[task.action]()
        print(f"executed {task.id}: {results[task.id]}")
    return results


async def main() -> None:
    plan = await ask(
        "Planner",
        "Plan a refund review using only supplied actions, in execution order.",
        f"Duplicate charge for order 42. Actions: {list(ACTIONS)}",
        Plan,
        {
            "tasks": [
                {"id": "invoice", "action": "read_invoice"},
                {"id": "policy", "action": "check_policy"},
                {
                    "id": "approval",
                    "action": "request_approval",
                    "depends_on": ["invoice", "policy"],
                },
            ]
        },
    )
    print(f"OK: completed={list(execute(plan))}")


if __name__ == "__main__":
    asyncio.run(main())
