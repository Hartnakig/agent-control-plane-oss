# Governance Model

This scaffold keeps governance simple.

## Formal Onboarding

A worker is treated as formal only when these files exist:

1. `worker-profile.json`
2. `status/controller-link.md`
3. `memory/session_memory.md`

## Registry Policy

The registry is generated from worker profiles. Do not treat the registry as the place to hand-edit worker metadata.

## Communication Policy

Prefer file classes such as:

- `task_from_supervisor_*.md`
- `handoff_from_supervisor_*.md`
- `status_from_subordinate_*.md`
- `deliverable_from_subordinate_*.md`

## Snapshot Policy

`_agent_profile` is for migration, recovery, and audit.

It should include:

- config summary
- environment manifest
- memory snapshot
- rules snapshot
- skills manifest

It should not include:

- secrets
- runtime caches
- logs
- databases
- raw session internals
