"""Fan in independent outputs through one deterministic merge node."""


def merge(findings: list[str]) -> dict[str, str]:
    blocked = [item for item in findings if "timeout" in item or "error" in item]
    return {
        "combined": "; ".join(sorted(findings)),
        "decision": "escalate" if blocked else "continue",
    }


def main() -> None:
    healthy = merge(["logs: ok", "status: healthy", "billing: clear"])
    degraded = merge(["logs: timeout", "status: healthy", "billing: clear"])
    print(f"OK: healthy={healthy['decision']} degraded={degraded['decision']}")


if __name__ == "__main__":
    main()
