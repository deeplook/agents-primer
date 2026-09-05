"""Map every important failure mode to a regression check and an owner."""


def main() -> None:
    matrix = {
        "wrong route": "test_router_selects_specialists",
        "unbounded loop": "test_bounded_loop_stops_and_rejects_overrun",
        "tool overreach": "test_privileged_tool_requires_approval",
        "unsafe input": "test_input_guardrail_rejects_unsafe_and_overlong",
        "internal leak": "test_output_guardrail_blocks_internal_leak",
    }
    print(f"OK: checks={matrix}")


if __name__ == "__main__":
    main()
