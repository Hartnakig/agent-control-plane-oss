from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .registry import get_profile_string, load_json, resolve_profile_path, walk_worker_profiles


def now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_profile_readme(alias: str, code: str, level: str) -> str:
    return "\n".join(
        [
            f"# {alias} _agent_profile",
            "",
            f"Generated: {now_string()}",
            "",
            "This directory is a portable worker profile snapshot for migration, recovery, and audit.",
            "",
            "## Included",
            "",
            "- config/config_snapshot.toml",
            "- environment/environment_manifest.md",
            "- memory/memory_sources.md",
            "- memory/session_memory_snapshot.md",
            "- rules/rules_manifest.md",
            "- rules/rules_snapshot/",
            "- skills/skills_manifest.md",
            "",
            "## Excluded",
            "",
            "- auth tokens or secrets",
            "- caches and temp files",
            "- runtime logs and pid files",
            "- databases or machine-bound session state",
            "",
            f"Worker code: {code}",
            f"Worker level: {level}",
        ]
    )


def build_config_snapshot(profile: dict[str, Any]) -> str:
    lines = [
        'generated_from = "worker-profile.json"',
        f'generated_at = "{now_string()}"',
        "",
        "[worker]",
        f'id = "{get_profile_string(profile, "worker_id", "id")}"',
        f'alias = "{get_profile_string(profile, "alias", "name")}"',
        f'assistant_code = "{get_profile_string(profile, "assistant_code", "code")}"',
        f'assistant_level = "{get_profile_string(profile, "assistant_level", "level")}"',
        f'window_title = "{get_profile_string(profile, "window_title")}"',
    ]
    return "\n".join(lines) + "\n"


def build_environment_manifest(profile: dict[str, Any], agent_root: Path, coordination_root: Path | None) -> str:
    lines = [
        "# Environment Manifest",
        "",
        f"Generated: {now_string()}",
        f"- Worker ID: {get_profile_string(profile, 'worker_id', 'id')}",
        f"- Alias: {get_profile_string(profile, 'alias', 'name')}",
        f"- Assistant code: {get_profile_string(profile, 'assistant_code', 'code')}",
        f"- Assistant level: {get_profile_string(profile, 'assistant_level', 'level')}",
        f"- Agent root: {agent_root}",
    ]
    if coordination_root:
        lines.append(f"- Coordination root: {coordination_root}")

    scope = profile.get("scope")
    lines.extend(["", "## Declared scope"])
    if isinstance(scope, list) and scope:
        lines.extend([f"- {item}" for item in scope])
    else:
        lines.append("- (none declared)")
    return "\n".join(lines) + "\n"


def build_memory_sources(memory_files: list[Path]) -> str:
    lines = ["# Memory Sources", "", f"Generated: {now_string()}", ""]
    if not memory_files:
        lines.append("- No memory files found.")
    else:
        lines.extend([f"- {path}" for path in memory_files])
    return "\n".join(lines) + "\n"


def build_session_memory_snapshot(memory_files: list[Path]) -> str:
    lines = ["# Session Memory Snapshot", "", f"Generated: {now_string()}", ""]
    if not memory_files:
        lines.append("No session memory files were found.")
        return "\n".join(lines) + "\n"

    for path in memory_files:
        lines.extend([f"## {path.name}", "", path.read_text(encoding="utf-8", errors="replace").strip(), ""])
    return "\n".join(lines).rstrip() + "\n"


def build_rules_manifest(rule_sources: list[Path]) -> str:
    lines = ["# Rules Manifest", "", f"Generated: {now_string()}", ""]
    if not rule_sources:
        lines.append("- No rule source files found.")
    else:
        lines.extend([f"- {path}" for path in rule_sources])
    return "\n".join(lines) + "\n"


def build_skills_manifest(agent_root: Path) -> str:
    skills_root = agent_root / "skills"
    skill_files = sorted(skills_root.rglob("SKILL.md")) if skills_root.exists() else []
    lines = ["# Skills Manifest", "", f"Generated: {now_string()}", ""]
    if not skill_files:
        lines.append("- No local skills found.")
    else:
        lines.extend([f"- {path}" for path in skill_files])
    return "\n".join(lines) + "\n"


def collect_memory_files(agent_root: Path) -> list[Path]:
    memory_root = agent_root / "memory"
    if not memory_root.exists():
        return []
    return sorted(path for path in memory_root.iterdir() if path.is_file() and path.suffix.lower() == ".md")


def collect_rule_sources(profile: dict[str, Any], profile_path: Path) -> list[Path]:
    rule_fields = (
        "staffing_standard_path",
        "communication_standard_path",
        "profile_standard_path",
        "reading_order_path",
        "memory_rule_path",
    )
    paths: list[Path] = []
    for field in rule_fields:
        value = get_profile_string(profile, field)
        if value:
            resolved = resolve_profile_path(value, profile_path)
            if resolved.exists():
                paths.append(resolved)
    return paths


def snapshot_worker_profile(profile_path: Path, coordination_root: Path | None = None) -> Path:
    profile = load_json(profile_path, default={}) or {}
    agent_root = resolve_profile_path(get_profile_string(profile, "agent_root"), profile_path)
    snapshot_root = agent_root / "_agent_profile"

    alias = get_profile_string(profile, "alias", "name") or "Worker"
    code = get_profile_string(profile, "assistant_code", "code") or "B_worker"
    level = get_profile_string(profile, "assistant_level", "level") or "B"

    memory_files = collect_memory_files(agent_root)
    rule_sources = collect_rule_sources(profile, profile_path)

    write_text(snapshot_root / "README.md", build_profile_readme(alias, code, level))
    write_text(snapshot_root / "config" / "config_snapshot.toml", build_config_snapshot(profile))
    write_text(
        snapshot_root / "environment" / "environment_manifest.md",
        build_environment_manifest(profile, agent_root, coordination_root),
    )
    write_text(snapshot_root / "memory" / "memory_sources.md", build_memory_sources(memory_files))
    write_text(snapshot_root / "memory" / "session_memory_snapshot.md", build_session_memory_snapshot(memory_files))
    write_text(snapshot_root / "rules" / "rules_manifest.md", build_rules_manifest(rule_sources))
    write_text(snapshot_root / "skills" / "skills_manifest.md", build_skills_manifest(agent_root))

    for source in rule_sources:
        target = snapshot_root / "rules" / "rules_snapshot" / source.name
        write_text(target, source.read_text(encoding="utf-8", errors="replace"))

    return snapshot_root


def snapshot_profiles(workers_root: Path, scan_roots: list[Path], coordination_root: Path | None = None) -> list[Path]:
    written: list[Path] = []
    seen: set[Path] = set()
    for root in [workers_root, *scan_roots]:
        for profile_path in walk_worker_profiles(root.resolve()):
            if profile_path in seen:
                continue
            seen.add(profile_path)
            written.append(snapshot_worker_profile(profile_path, coordination_root=coordination_root))
    return written
