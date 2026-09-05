"""Give parallel specialists the same scoped brief, not unrelated fragments."""


def consistent(left: dict[str, str], right: dict[str, str], keys: set[str]) -> bool:
    return all(left.get(key) == right.get(key) for key in keys)


def main() -> None:
    brief = {"account": "Ada", "issue": "duplicate charge", "policy_version": "2026-01"}
    billing_context = {**brief, "task": "verify charge"}
    policy_context = {**brief, "task": "check refund rule"}
    fragmented_billing = {"account": "Ada", "task": "verify charge"}
    fragmented_policy = {"issue": "duplicate charge", "task": "check refund rule"}
    shared_keys = {"account", "issue", "policy_version"}
    print(
        "OK: "
        f"shared={consistent(billing_context, policy_context, shared_keys)} "
        f"fragmented={consistent(fragmented_billing, fragmented_policy, shared_keys)}"
    )


if __name__ == "__main__":
    main()
