# Agents Primer

Small Python lessons for designing bounded, observable agent workflows with the
OpenAI Agents SDK. It complements `openai-primer`: that project explains direct
API capabilities; this one focuses on control flow around agent calls.

The SDK's core objects are `Agent` (a model plus instructions, tools, and
handoffs) and `Runner` (the loop that calls the model, executes tools, and
follows handoffs). Guardrails, sessions, tracing, and MCP servers attach to
those objects. This primer uses them in `01`, `02`, `04`, `12`, and `13`. The
other lessons implement the same workflow ideas in ordinary Python so routing,
budgets, approval, and failure edges stay deterministic.

## Setup

```bash
uv sync --all-groups
export OPENAI_API_KEY="..."
uv run python examples/01_first_agent.py
```

SDK-backed examples print `SKIP` without an API key. The workflow and graph
examples are deterministic, run offline, and exercise both the allowed path
and the rejected or fallback path for each control-flow idea.

## Modules

| File | Topic |
|---|---|
| `01_first_agent.py` | Define and run one agent |
| `02_function_tool.py` | Typed Python function tool |
| `03_sequential_pipeline.py` | Explicit sequential workflow |
| `04_conditional_router.py` | Deterministic branch selection |
| `05_typed_state.py` | Shared typed workflow state |
| `06_bounded_loop.py` | Max-iteration loop guard |
| `07_retry_fallback.py` | Retry and fallback edge |
| `08_fan_out.py` | Parallel specialist fan-out |
| `09_fan_in.py` | Merge independent results |
| `10_evaluator_refiner.py` | Bounded evaluate/refine cycle |
| `11_plan_execute.py` | Plan then execute explicit steps |
| `12_handoff.py` | Route to a specialist agent |
| `13_agent_as_tool.py` | Keep a manager in control |
| `14_input_guardrail.py` | Reject unsafe or off-scope inputs |
| `15_human_approval.py` | Pause at an approval boundary |
| `16_graph_topology.py` | Represent workflow nodes and edges explicitly |
| `17_state_machine.py` | Drive a workflow through named states |
| `18_cycle_detection.py` | Reject accidental cyclic dependencies |
| `19_time_budget.py` | Stop work when a time budget is exceeded |
| `20_checkpoint_resume.py` | Save and resume workflow state locally |
| `21_handoff_payload.py` | Minimize context passed to a specialist |
| `22_output_guardrail.py` | Validate a result before delivery |
| `23_edge_tracing.py` | Record node and edge events for debugging |
| `24_failure_edges.py` | Route expected failure to a fallback node |
| `25_manager_worker.py` | Delegate bounded work while the manager owns output |
| `26_concurrency_budget.py` | Limit parallel work deliberately |
| `27_cancellation.py` | Stop downstream work after a terminal decision |
| `28_mcp_boundary.py` | Model MCP as a privileged graph boundary |
| `29_capstone_triage.py` | Run a bounded support-triage workflow |
| `30_capability_map.py` | Design graph nodes from grouped capabilities |
| `31_shared_context.py` | Give parallel specialists a consistent brief |
| `32_conflict_resolution.py` | Reconcile incompatible specialist findings |
| `33_context_compression.py` | Preserve a compact state summary between loops |
| `34_error_feedback.py` | Feed a tool failure into the next workflow step |
| `35_failure_modes.py` | Inventory failure modes before writing an eval |
| `36_success_metrics.py` | Define measurable workflow success criteria |
| `37_eval_matrix.py` | Link failure modes to regression checks |
| `38_regression_eval.py` | Run a deterministic workflow regression suite |
| `39_tool_access.py` | Apply least privilege to graph nodes |
| `40_lethal_trifecta.py` | Detect unsafe input/data/action combinations |
| `41_sandbox_boundary.py` | Define a constrained code-execution boundary |

Run `make check-all` for the offline quality gate: formatting, linting, strict typing, and tests. `make live-core` makes a
small number of real SDK calls and uses API credits.

## Further reading

- [OpenAI Agents SDK guide](https://developers.openai.com/api/docs/guides/agents)
- [Agents SDK orchestration](https://developers.openai.com/api/docs/guides/agents/orchestration)
