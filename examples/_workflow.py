"""Tiny deterministic workflow primitives used by the graph-pattern lessons."""

from collections.abc import Callable
from dataclasses import dataclass, field

TOOL_PERMISSIONS: dict[str, frozenset[str]] = {
    "research_agent": frozenset({"search_documents"}),
    "refund_agent": frozenset({"read_invoice", "request_refund_approval"}),
}


@dataclass
class WorkflowState:
    request: str
    route: str | None = None
    attempts: int = 0
    notes: list[str] = field(default_factory=list)


def classify_request(request: str) -> str:
    lowered = request.lower()
    if "refund" in lowered or "invoice" in lowered:
        return "billing"
    if "error" in lowered or "broken" in lowered:
        return "technical"
    return "general"


def input_allowed(request: str) -> bool:
    return 0 < len(request) <= 120 and "delete account" not in request.lower()


def output_deliverable(text: str) -> bool:
    return text.startswith("Answer:") and "internal" not in text.lower()


def run_bounded(action: Callable[[int], bool], *, limit: int) -> int:
    for attempt in range(1, limit + 1):
        if action(attempt):
            return attempt
    raise RuntimeError(f"workflow exceeded its {limit}-iteration limit")


def tool_allowed(agent: str, tool: str) -> bool:
    return tool in TOOL_PERMISSIONS.get(agent, frozenset())


def is_lethal_trifecta(
    *, untrusted_input: bool, sensitive_data: bool, external_action: bool
) -> bool:
    return untrusted_input and sensitive_data and external_action
