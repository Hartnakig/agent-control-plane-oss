# Coordination Hub

This directory is the file-based command center for the open-source example workspace.

## Roles

- `controller`: assigns work and accepts results
- `worker-*`: executes tasks and reports back

## Standard Directories

- `tasks/`: task cards
- `results/`: worker submissions
- `acceptance/`: controller decisions
- `prompts/`: bootstrap prompts for new worker sessions
- `runtime/`: optional runtime state

## Operating Rules

1. Every worker keeps a stable worker ID.
2. Every formal task should exist as a file, not only in chat.
3. Workers do not self-accept their own results.
4. The registry should be rebuilt from `worker-profile.json` files.

## Registry

The canonical worker registry lives in `registry.json`.
