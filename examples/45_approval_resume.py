"""Persist approval across invocations; one SQLite transaction prevents replay.

Run prepare, then approve or reject with the same --db path. No arguments runs
an isolated offline demo. The ledger is simulated: remote APIs also need an
idempotency key and reconciliation after uncertain responses.
"""

import argparse
import sqlite3
import tempfile
from pathlib import Path


def transition(path: Path, command: str) -> tuple[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    try:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS approval (id TEXT PRIMARY KEY, status TEXT)"
        )
        connection.execute(
            "CREATE TABLE IF NOT EXISTS ledger (id TEXT PRIMARY KEY, amount INTEGER)"
        )
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            if command == "prepare":
                connection.execute(
                    "INSERT OR IGNORE INTO approval VALUES ('refund-42', 'pending')"
                )
            row = connection.execute(
                "SELECT status FROM approval WHERE id='refund-42'"
            ).fetchone()
            if row is None:
                raise ValueError("prepare the action first")
            status = str(row[0])
            if command in {"approve", "reject"} and status == "pending":
                status = "executed" if command == "approve" else "rejected"
                if command == "approve":
                    connection.execute("INSERT INTO ledger VALUES ('refund-42', 20)")
                connection.execute(
                    "UPDATE approval SET status=? WHERE id='refund-42'", (status,)
                )
            count = int(connection.execute("SELECT count(*) FROM ledger").fetchone()[0])
        return status, count
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", choices=["prepare", "approve", "reject"])
    parser.add_argument("--db", type=Path, default=Path("out/approval.sqlite"))
    args = parser.parse_args()
    if args.command:
        print(f"OK: {transition(args.db, args.command)}")
    else:
        with tempfile.TemporaryDirectory() as directory:
            for command in ["prepare", "approve", "approve"]:
                print(
                    f"OK: {command} -> {transition(Path(directory) / 'demo.sqlite', command)}"
                )


if __name__ == "__main__":
    main()
