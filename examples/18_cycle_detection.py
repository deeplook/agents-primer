"""Detect cycles in a planned workflow before an agent can enter one."""


def has_cycle(graph: dict[str, list[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        cyclic = any(visit(child) for child in graph[node])
        visiting.remove(node)
        visited.add(node)
        return cyclic

    return any(visit(node) for node in graph)


def main() -> None:
    acyclic = {"plan": ["execute"], "execute": ["evaluate"], "evaluate": []}
    cyclic = {"plan": ["execute"], "execute": ["evaluate"], "evaluate": ["plan"]}
    if has_cycle(cyclic) and not has_cycle(acyclic):
        print("OK: rejected cyclic plan -> execute -> evaluate -> plan")
        return
    raise RuntimeError("cycle detector missed a loop")


if __name__ == "__main__":
    main()
