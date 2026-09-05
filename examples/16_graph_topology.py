"""Keep graph topology as data so it can be inspected before running."""


def dangling(graph: dict[str, list[str]]) -> list[str]:
    return [dst for edges in graph.values() for dst in edges if dst not in graph]


def main() -> None:
    graph = {
        "intake": ["route"],
        "route": ["billing", "technical", "general"],
        "billing": ["synthesize"],
        "technical": ["synthesize"],
        "general": ["synthesize"],
        "synthesize": [],
    }
    broken = {**graph, "billing": ["missing_node"]}
    print(
        f"OK: nodes={len(graph)} route_edges={graph['route']} "
        f"valid_dangling={dangling(graph)} invalid_dangling={dangling(broken)}"
    )


if __name__ == "__main__":
    main()
