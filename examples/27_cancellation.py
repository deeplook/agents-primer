"""A terminal graph decision cancels downstream work before it finishes."""

import asyncio


async def issue_refund(started: asyncio.Event, released: asyncio.Event) -> str:
    started.set()
    await released.wait()
    return "refund issued"


async def main() -> None:
    account_closed = True
    started = asyncio.Event()
    released = asyncio.Event()
    task = asyncio.create_task(issue_refund(started, released))
    await started.wait()
    if account_closed:
        task.cancel()
        cancelled = False
        try:
            await task
        except asyncio.CancelledError:
            cancelled = True
        print(f"OK: next_node=stop cancelled={cancelled} released={released.is_set()}")
        return
    released.set()
    print("OK:", await task)


if __name__ == "__main__":
    asyncio.run(main())
