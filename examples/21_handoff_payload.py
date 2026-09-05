"""Pass the minimum useful context across a specialist handoff edge."""


def main() -> None:
    request = {"customer": "Ada", "issue": "refund", "internal_notes": "do not share"}
    handoff = {key: request[key] for key in ("customer", "issue")}
    dropped = sorted(set(request) - set(handoff))
    print(f"OK: handoff={handoff} dropped={dropped}")


if __name__ == "__main__":
    main()
