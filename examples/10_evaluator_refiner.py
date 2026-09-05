"""Use a bounded evaluator/refiner cycle instead of unbounded self-correction."""


def acceptable(text: str) -> bool:
    return text.endswith(".") and "please" not in text.lower() and len(text) <= 40


def refine(text: str) -> str:
    cleaned = text.replace("please ", "", 1)
    if not cleaned.endswith("."):
        cleaned = cleaned.rstrip("!") + "."
    return cleaned


def main() -> None:
    draft = "please please reset the password!"
    for attempt in range(1, 4):
        if acceptable(draft):
            print(f"OK: accepted={draft!r} attempt={attempt}")
            return
        draft = refine(draft)
    raise RuntimeError("refinement budget exhausted")


if __name__ == "__main__":
    main()
