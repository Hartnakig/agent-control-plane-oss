from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "runtime",
    "logs",
    "tmp",
}

LEVEL_ORDER = {
    "A": 0,
    "S": 1,
    "B": 1,
    "C": 2,
    "D": 3,
}


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_profile_path(value: str | None, profile_path: Path) -> Path:
    if not value:
        return profile_path.parent
    path = Path(value)
    if path.is_absolute():
        return path
    return (profile_path.parent / path).resolve()


def get_profile_string(profile: dict[str, Any], *names: str) -> str:
    for name in names:
        value = profile.get(name)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def walk_worker_profiles(root: Path) -> list[Path]:
    if not root.exists():
        return []

    paths: list[Path] = []
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in IGNORED_DIRS]
        if "worker-profile.json" in files:
            paths.append(Path(current_root) / "worker-profile.json")
    return sorted(set(paths))


def default_contact_mode(agent_root: Path, workers_root: Path) -> list[str]:
    try:
        agent_root.relative_to(workers_root.resolve())
        return ["coordination_files", "background_exec", "local_workspace"]
    except ValueError:
        return ["coordination_files", "agent_window", "background_exec"]


def default_background_worker(agent_root: Path, workers_root: Path) -> dict[str, Any]:
    try:
        agent_root.relative_to(workers_root.resolve())
        return {
            "enabled": True,
            "mode": "daemon",
            "poll_seconds": 15,
            "idle_exit_seconds": 0,
            "autostart_on_task": False,
        }
    except ValueError:
        return {
            "enabled": True,
            "mode": "ondemand",
            "poll_seconds": 15,
            "idle_exit_seconds": 120,
            "autostart_on_task": True,
        }


def merge_worker_record(
    profile: dict[str, Any],
    profile_path: Path,
    existing: dict[str, Any] | None,
    coordination_root: Path,
    workers_root: Path,
) -> dict[str, Any]:
    worker_id = get_profile_string(profile, "worker_id", "id")
    assistant_code = get_profile_string(profile, "assistant_code", "code")
    assistant_level = get_profile_string(profile, "assistant_level", "level")
    alias = get_profile_string(profile, "alias", "name")
    window_title = get_profile_string(profile, "window_title")
    project_root = resolve_profile_path(get_profile_string(profile, "project_root"), profile_path)
    agent_root = resolve_profile_path(get_profile_string(profile, "agent_root"), profile_path)
    status = get_profile_string(profile, "status") or "registered"

    record: dict[str, Any] = {
        "id": worker_id,
        "alias": alias,
        "assistant_code": assistant_code,
        "assistant_level": assistant_level,
        "window_title": window_title,
        "project_root": str(project_root),
        "agent_root": str(agent_root),
        "status": status,
        "contact_mode": default_contact_mode(agent_root, workers_root),
        "background_worker": default_background_worker(agent_root, workers_root),
        "coordination_root": str(coordination_root.resolve()),
    }

    for field in ("supervisor_worker_id", "supervisor_assistant_code"):
        value = get_profile_string(profile, field)
        if value:
            record[field] = value

    scope = profile.get("scope")
    if isinstance(scope, list) and scope:
        record["scope"] = [str(item) for item in scope]

    if existing:
        if isinstance(existing.get("scope"), list) and "scope" not in record:
            record["scope"] = [str(item) for item in existing["scope"]]
        if isinstance(existing.get("contact_mode"), list):
            record["contact_mode"] = [str(item) for item in existing["contact_mode"]]
        if isinstance(existing.get("background_worker"), dict):
            merged_worker = dict(record["background_worker"])
            merged_worker.update(existing["background_worker"])
            record["background_worker"] = merged_worker

    return record


def default_controller(coordination_root: Path) -> dict[str, Any]:
    return {
        "id": "controller",
        "role": "controller",
        "assistant_code": "A_controller",
        "assistant_level": "A",
        "display_name": "Controller",
        "workspace": str(coordination_root.resolve()),
        "authority": ["assign", "verify", "accept", "reject", "close"],
    }


def worker_sort_key(worker: dict[str, Any]) -> tuple[int, str, str]:
    level = str(worker.get("assistant_level", "")).upper()
    assistant_code = str(worker.get("assistant_code", ""))
    worker_id = str(worker.get("id", ""))
    return (LEVEL_ORDER.get(level, 9), assistant_code, worker_id)


def sync_registry(
    coordination_root: Path,
    workers_root: Path,
    scan_roots: list[Path],
    registry_path: Path | None = None,
) -> dict[str, Any]:
    coordination_root = coordination_root.resolve()
    workers_root = workers_root.resolve()
    registry_path = registry_path or coordination_root / "registry.json"

    existing_registry = load_json(registry_path, default={}) or {}
    existing_workers = {
        str(worker.get("id")): worker
        for worker in existing_registry.get("workers", [])
        if isinstance(worker, dict) and worker.get("id")
    }

    discovered: dict[str, dict[str, Any]] = {}
    for root in [workers_root, *scan_roots]:
        for profile_path in walk_worker_profiles(root.resolve()):
            profile = load_json(profile_path, default={}) or {}
            worker_id = get_profile_string(profile, "worker_id", "id")
            assistant_code = get_profile_string(profile, "assistant_code", "code")
            if not worker_id or not assistant_code:
                continue
            discovered[worker_id] = merge_worker_record(
                profile=profile,
                profile_path=profile_path,
                existing=existing_workers.get(worker_id),
                coordination_root=coordination_root,
                workers_root=workers_root,
            )

    payload = {
        "controller": existing_registry.get("controller") or default_controller(coordination_root),
        "workers": sorted(discovered.values(), key=worker_sort_key),
    }
    write_json(registry_path, payload)
    return payload
