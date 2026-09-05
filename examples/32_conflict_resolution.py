"""Resolve conflicting specialist claims through an explicit merge policy."""


def resolve(findings: list[dict[str, object]], *, authority: str) -> dict[str, object]:
    try:
        return next(item for item in findings if item["source"] == authority)
    except StopIteration as error:
        raise RuntimeError(
            f"no finding from authoritative source {authority}"
        ) from error


def main() -> None:
    findings = [
        {"source": "ledger", "amount": 20},
        {"source": "email", "amount": 25},
    ]
    chosen = resolve(findings, authority="ledger")
    discarded = [item for item in findings if item["source"] != "ledger"]
    print(f"OK: chosen={chosen} discarded={discarded} reason=ledger_is_authoritative")


if __name__ == "__main__":
    main()
