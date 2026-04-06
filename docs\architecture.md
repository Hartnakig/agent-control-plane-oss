# Architecture

The control plane has three layers:

## 1. Coordination Layer

The coordination layer holds shared process files:

- task cards
- result submissions
- acceptance decisions
- bootstrap prompts
- the synced registry

This layer is intentionally plain text and JSON so it can be inspected, diffed, and recovered.

## 2. Worker Body Layer

Each worker has a body directory that stores:

- identity
- memory
- governance references
- formal inbox and outbox files
- a portable `_agent_profile` snapshot

The worker body should stay lightweight. Heavy code, large datasets, runtime logs, and caches belong in project workspaces, not in the body directory.

## 3. Project Layer

Projects can carry their own `_agent` directory with a project worker and optional subworkers.

This lets a project define:

- its own worker memory
- project-specific coordination
- subordinate worker relationships

## Why This Shape Works

- workers are easy to register
- governance stays inspectable
- migration is simple
- partial failure is survivable because files remain the source of truth
