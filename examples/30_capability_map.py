"""Design graph nodes by grouping capabilities before naming agents."""


def nodes_from_capabilities(capabilities: dict[str, str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for capability, node in capabilities.items():
        grouped.setdefault(node, []).append(capability)
    return grouped


def main() -> None:
    capabilities = {
        "search knowledge base": "research",
        "read account history": "research",
        "draft response": "resolution",
        "request refund approval": "resolution",
    }
    grouped = nodes_from_capabilities(capabilities)
    print(f"OK: nodes={sorted(grouped)} grouped={grouped}")


if __name__ == "__main__":
    main()
