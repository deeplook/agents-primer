# Changelog

## [0.2.0] - 2026-09-09

### Added
- Focused lessons for partial failure, dependency scheduling, bounded replanning,
  and persistent approval with a transactional simulated ledger.
- Offline behavioral tests for orchestration boundaries and optional live SDK execution.

### Changed
- Replaced workflow sketches with SDK tools, context, handoffs, guardrails,
  approvals, RunState persistence, hooks, MCP, and typed evaluations.
- Offline model lessons now use SDK ScriptedModel with the real Runner; real
  API calls consistently require --live. Added live-orchestration and live-all.
- Declared the SDK 0.22 and MCP 2 minimums used by the examples, and labeled
  supporting Python exercises and configuration-only lessons explicitly.
- Deepened fan-out, evaluator/refiner, and plan/execute with typed model outputs
  and visible orchestration shared by scripted and live runs.

## [0.1.0] - 2026-09-06

### Changed
- Prepared the repository for public release with a GitHub-first badge policy
  and a strict static-type-checking quality gate.
- Pinned CI to Python 3.12 with locked dependency synchronization.
