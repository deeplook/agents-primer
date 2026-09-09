# Agents Primer

[![CI](https://github.com/deeplook/agents-primer/actions/workflows/check.yml/badge.svg)](https://github.com/deeplook/agents-primer/actions/workflows/check.yml)
[![Downloads](https://img.shields.io/github/downloads/deeplook/agents-primer/total?label=Downloads&logo=github)](https://github.com/deeplook/agents-primer/releases)
[![License](https://img.shields.io/github/license/deeplook/agents-primer?logo=github)](LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/deeplook)

Small Python lessons for designing bounded, observable agent workflows with the
OpenAI Agents SDK. It complements `openai-primer`: that project explains direct
API capabilities; this one focuses on control flow around agent calls.

The SDK's core objects are `Agent` (instructions, model, tools, and handoffs)
and `Runner` (model turns, tool execution, handoffs, and interruptions). The
lessons use SDK context, typed outputs, guardrails, approvals, `RunState`,
lifecycle hooks, tracing, and MCP directly. Python supplies scheduling and
application policies around those SDK calls.

**Offline does not mean skipping the SDK.** Model-running examples always use
the real `Runner`. By default, the SDK's `ScriptedModel` supplies responses and
tool calls; the SDK still executes tools, follows handoffs, checks guardrails,
and handles approval/resumption. `--live` switches only the model to the API.
Offline runs disable trace export, even when an API key is present.

Two lessons inspect SDK configuration: `16` shows the actual handoff graph,
and `41` configures hosted code execution (only `--live` starts a container).
Four supporting Python exercises are explicitly separate: `18` validates graph
cycles, `35` inventories failures, `37` maps failures to SDK tests, and `45`
demonstrates a transactional ledger across process restarts. For SDK approval
and serialized run state, see `15` and `20` respectively.

## Setup

```bash
uv sync --all-groups
uv run python examples/01_first_agent.py

# Optional real API calls; these use API credits.
export OPENAI_API_KEY="..."
export OPENAI_AGENT_MODEL=gpt-5-nano
uv run python examples/01_first_agent.py --live
```

The default model for live runs is `gpt-5-mini`; override it with
`OPENAI_AGENT_MODEL`. Explicit live runs fail if the API key is missing.
The locked environment uses Agents SDK 0.22, including `agents.testing`, and MCP 2.

## Modules

| File | Topic |
|---|---|
| `01_first_agent.py` | Define and run one agent |
| `02_function_tool.py` | Typed Python function tool |
| `03_sequential_pipeline.py` | Explicit sequential workflow |
| `04_conditional_router.py` | Deterministic branch selection |
| `05_typed_state.py` | Typed SDK context accessed by a function tool |
| `06_bounded_loop.py` | SDK max-turn limit and exception |
| `07_retry_fallback.py` | Retry and fallback edge |
| `08_fan_out.py` | Parallel specialist fan-out |
| `09_fan_in.py` | Merge independent results |
| `10_evaluator_refiner.py` | Bounded evaluate/refine cycle |
| `11_plan_execute.py` | Plan then execute explicit steps |
| `12_handoff.py` | Route to a specialist agent |
| `13_agent_as_tool.py` | Keep a manager in control |
| `14_input_guardrail.py` | SDK input guardrail before model execution |
| `15_human_approval.py` | SDK tool approval, rejection, and resumption |
| `16_graph_topology.py` | Inspect SDK handoff configuration |
| `17_state_machine.py` | Drive a workflow through named states |
| `18_cycle_detection.py` | Supporting Python: reject cyclic dependencies |
| `19_time_budget.py` | Stop work when a time budget is exceeded |
| `20_checkpoint_resume.py` | Serialize and restore SDK RunState |
| `21_handoff_payload.py` | Typed handoff arguments and history filtering |
| `22_output_guardrail.py` | SDK output guardrail and tripwire |
| `23_edge_tracing.py` | SDK handoff hooks and workflow traces |
| `24_failure_edges.py` | Route expected failure to a fallback node |
| `25_manager_worker.py` | Manager delegates, supplies follow-up, and owns typed output |
| `26_concurrency_budget.py` | Limit parallel work deliberately |
| `27_cancellation.py` | Stop downstream work after a terminal decision |
| `28_mcp_boundary.py` | Real local MCP server, allowlist, and SDK approval |
| `29_capstone_triage.py` | Compose SDK guardrails, handoff, and approval/resumption |
| `30_capability_map.py` | Design graph nodes from grouped capabilities |
| `31_shared_context.py` | Give parallel specialists a consistent brief |
| `32_conflict_resolution.py` | Reconcile incompatible specialist findings |
| `33_context_compression.py` | Preserve a compact state summary between loops |
| `34_error_feedback.py` | Feed a tool failure into the next workflow step |
| `35_failure_modes.py` | Supporting Python: inventory failure modes |
| `36_success_metrics.py` | Measure typed SDK routing outcomes and model turns |
| `37_eval_matrix.py` | Supporting Python: map failures to SDK regression tests |
| `38_regression_eval.py` | Assert routing outcomes from SDK runs |
| `39_tool_access.py` | SDK enforcement of an agent's available tools |
| `40_lethal_trifecta.py` | SDK tool guardrail using application trust labels |
| `41_sandbox_boundary.py` | Configure SDK hosted code execution; opt-in live container |
| `42_partial_failure.py` | Retain specialist findings after an optional timeout |
| `43_dependency_scheduling.py` | Run ready agent tasks in waves with parent results |
| `44_replanning.py` | Replace failed work without replaying completed actions |
| `45_approval_resume.py` | Supporting Python: transactional approval ledger across processes |

## Concise orchestration examples

Start with `08` (parallel specialists and synthesis), `10` (typed critique and
bounded revision), and `11` (validated plans). Continue with `42`–`45` for failure,
dependencies, replanning, and persistent approval. Each keeps control flow visible;
`_orchestration.py` shares typed single-agent runs and task/plan contracts.
`25` adds manager-directed worker follow-up; `29` composes multiple SDK features.

### Async and concurrent agent execution

With `--live`, these examples run independent agents concurrently through the
SDK's asynchronous `Runner.run()` calls:

- `08_fan_out.py` uses `asyncio.gather()` to run two specialists concurrently,
  then passes both findings to a synthesizer agent.
- `42_partial_failure.py` uses `asyncio.gather(return_exceptions=True)` to retain
  successful findings when an optional specialist times out.
- `43_dependency_scheduling.py` uses `asyncio.TaskGroup` to run ready tasks
  concurrently. Dependent agents receive their prerequisites' results in a later
  wave; a failed wave cancels its sibling tasks and prevents downstream execution.

Async calls alone do not imply concurrency: awaiting each agent in a loop runs
them sequentially. Here, `gather()` and `TaskGroup` schedule overlapping work.
This is useful for independent investigations because network waits overlap;
it does not inherently reduce token costs and increases simultaneous API demand.

Offline mode also runs these SDK workflows, using the SDK's scripted model
without provider requests. Tests separately verify concurrent specialist startup,
dependency ordering, and cancellation.

### Running the examples

```bash
uv run python examples/08_fan_out.py         # scripted, offline, no credits
uv run python examples/08_fan_out.py --live  # real SDK calls; requires API key
uv run python examples/43_dependency_scheduling.py
uv run python examples/43_dependency_scheduling.py --live  # concurrent ready agents
uv run python examples/45_approval_resume.py prepare --db out/review.sqlite
uv run python examples/45_approval_resume.py approve --db out/review.sqlite
uv run python examples/45_approval_resume.py approve --db out/review.sqlite
```

The repeated approval leaves one ledger entry. Use `reject` instead of `approve`
to demonstrate rejection; use a fresh database path for a new scenario. Running
`45` without arguments uses a temporary database and leaves no persistent state.
This is application-level persistence, not serialization of an SDK run. The
simulated ledger and approval update share a SQLite transaction; external effects
would additionally require idempotency keys and reconciliation.

Offline responses are fixtures, not model evaluations. Tests inject alternate
responses and failures into the same SDK orchestration. Model runs have explicit
turn limits (usually three; the manager and capstone allow four). `10` also limits
revision rounds and `44` permits one replan. These are not token or dollar budgets.
`42` deliberately injects an optional timeout even in live mode. Tools in `11`
and `44` remain simulated. No example moves money or contacts a customer.
`28` starts a local read-only MCP subprocess in both modes. `41 --live` uses a
hosted code container and incurs container charges in addition to model tokens;
it is deliberately excluded from `live-all`.

`43` deliberately uses wave scheduling: it waits for the whole ready batch before
starting the next batch. It validates cycles before execution and cancels sibling
tasks when a wave fails. `11` accepts ordered plans; `44` focuses on independent
remaining tasks, leaving dependency-aware replanning to a larger application.

Run `make check-all` for formatting, linting, strict typing, offline SDK behavior
tests, and smoke execution of all 45 lessons. Offline examples never print `SKIP`.

```bash
OPENAI_AGENT_MODEL=gpt-5-nano make live-core           # original five lessons
OPENAI_AGENT_MODEL=gpt-5-nano make live-orchestration  # seven orchestration lessons
OPENAI_AGENT_MODEL=gpt-5-nano make live-all            # all model lessons except hosted sandbox
```

All live targets require `OPENAI_API_KEY` and stop on the first failing process.
They are smoke runs; example `38` additionally asserts routing accuracy. Offline
tests verify SDK mechanics, not the quality or reliability of a live model.

## Further reading

- [OpenAI Agents SDK guide](https://developers.openai.com/api/docs/guides/agents)
- [Agents SDK orchestration](https://developers.openai.com/api/docs/guides/agents/orchestration)
