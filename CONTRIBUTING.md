# Contributing

Thanks for helping improve Agent Control Plane.

## Good First Contributions

- improve examples
- tighten schemas
- add validation commands
- add cross-platform runtime helpers
- improve docs and onboarding

## Local Setup

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e .
```

## Run Tests

```powershell
python -m unittest discover -s tests -v
```

## CLI Smoke Checks

```powershell
agent-control-plane sync-registry --coord-root coordination --workers-root examples/local-workers --scan-root examples/projects
agent-control-plane snapshot-profiles --coord-root coordination --workers-root examples/local-workers --scan-root examples/projects
```

## Contribution Guidelines

- keep changes scoped
- prefer plain, inspectable file formats
- avoid adding heavy infrastructure unless it clearly unlocks a real use case
- preserve the project's file-first design
- include tests when behavior changes

## Pull Requests

Please include:

- what changed
- why it changed
- how you tested it
- any follow-up risks or open questions
