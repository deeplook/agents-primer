"""Block the risky combination of untrusted input, sensitive data, and action."""

from _workflow import is_lethal_trifecta


def main() -> None:
    blocked = is_lethal_trifecta(
        untrusted_input=True, sensitive_data=True, external_action=True
    )
    read_only = is_lethal_trifecta(
        untrusted_input=True, sensitive_data=True, external_action=False
    )
    no_secrets = is_lethal_trifecta(
        untrusted_input=True, sensitive_data=False, external_action=True
    )
    trusted = is_lethal_trifecta(
        untrusted_input=False, sensitive_data=True, external_action=True
    )
    print(
        f"OK: all_three_blocked={blocked} "
        f"read_only_allowed={not read_only} "
        f"no_secrets_allowed={not no_secrets} "
        f"trusted_allowed={not trusted}"
    )


if __name__ == "__main__":
    main()
