# Worker A _agent_profile

Generated: 2026-04-06 20:37:05

This directory is a portable worker profile snapshot for migration, recovery, and audit.

## Included

- config/config_snapshot.toml
- environment/environment_manifest.md
- memory/memory_sources.md
- memory/session_memory_snapshot.md
- rules/rules_manifest.md
- rules/rules_snapshot/
- skills/skills_manifest.md

## Excluded

- auth tokens or secrets
- caches and temp files
- runtime logs and pid files
- databases or machine-bound session state

Worker code: D_worker_a
Worker level: D