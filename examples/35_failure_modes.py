"""List concrete workflow failures before attempting to evaluate quality."""


def main() -> None:
    failure_modes = {
        "wrong route": "billing request classified as general",
        "unbounded loop": "refiner never satisfies evaluator",
        "tool overreach": "research node calls refund tool",
        "unsafe input": "delete-account request reaches a specialist",
        "internal leak": "reply includes internal account identifiers",
    }
    print(f"OK: to_eval={list(failure_modes)}")


if __name__ == "__main__":
    main()
