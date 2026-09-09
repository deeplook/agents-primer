"""Map every important failure mode to a regression check and an owner."""


def main() -> None:
    matrix = {
        "wrong route": "test_sdk_routing_eval",
        "unbounded loop": "test_sdk_turn_limit",
        "tool overreach": "test_sdk_rejects_unknown_tool",
        "unsafe input": "test_sdk_input_guardrail_prevents_model_call",
        "internal leak": "test_sdk_output_guardrail",
    }
    print(f"OK: checks={matrix}")


if __name__ == "__main__":
    main()
