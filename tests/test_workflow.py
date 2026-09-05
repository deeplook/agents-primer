import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))

from _workflow import (
    classify_request,
    input_allowed,
    is_lethal_trifecta,
    output_deliverable,
    run_bounded,
    tool_allowed,
)


def test_router_selects_specialists() -> None:
    assert classify_request("My invoice needs a refund") == "billing"
    assert classify_request("The app shows an error") == "technical"
    assert classify_request("What are your hours?") == "general"


def test_bounded_loop_stops_and_rejects_overrun() -> None:
    assert run_bounded(lambda attempt: attempt == 2, limit=3) == 2
    try:
        run_bounded(lambda _attempt: False, limit=1)
    except RuntimeError as error:
        assert "exceeded" in str(error)
    else:
        raise AssertionError("expected bounded loop to fail")


def test_input_guardrail_rejects_unsafe_and_overlong() -> None:
    assert input_allowed("Please reset my password.")
    assert not input_allowed("Please delete account now.")
    assert not input_allowed("x" * 121)


def test_output_guardrail_blocks_internal_leak() -> None:
    assert output_deliverable("Answer: Your refund is being reviewed.")
    assert not output_deliverable("Answer: internal account 12 is past due.")
    assert not output_deliverable("Sure, we can do that.")


def test_privileged_tool_requires_approval() -> None:
    assert tool_allowed("research_agent", "search_documents")
    assert not tool_allowed("research_agent", "request_refund_approval")
    assert tool_allowed("refund_agent", "request_refund_approval")


def test_lethal_trifecta_only_blocks_all_three() -> None:
    assert is_lethal_trifecta(
        untrusted_input=True, sensitive_data=True, external_action=True
    )
    assert not is_lethal_trifecta(
        untrusted_input=True, sensitive_data=True, external_action=False
    )
    assert not is_lethal_trifecta(
        untrusted_input=True, sensitive_data=False, external_action=True
    )
    assert not is_lethal_trifecta(
        untrusted_input=False, sensitive_data=True, external_action=True
    )
