# Worker Profile

Every formal worker should have a `worker-profile.json`.

## Required Fields

- `worker_id`
- `alias`
- `assistant_code`
- `assistant_level`
- `project_root`
- `agent_root`

## Recommended Fields

- `window_title`
- `status`
- `scope`
- `supervisor_worker_id`
- `supervisor_assistant_code`
- `staffing_standard_path`
- `communication_standard_path`
- `profile_standard_path`

## Example

```json
{
  "worker_id": "worker-profile-manager",
  "alias": "Profile Manager",
  "assistant_code": "B_profile_manager",
  "assistant_level": "B",
  "window_title": "Profile Manager",
  "project_root": "..",
  "agent_root": ".",
  "status": "registered",
  "scope": [
    "Maintain worker profiles",
    "Maintain portable profile snapshots"
  ]
}
```

## Path Rules

Paths may be absolute or relative.

If a path is relative, this project resolves it relative to the directory that contains `worker-profile.json`.
