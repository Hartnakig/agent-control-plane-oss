from __future__ import annotations

import argparse
from pathlib import Path

from .registry import sync_registry
from .snapshot import snapshot_profiles


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-control-plane")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync-registry", help="Scan worker profiles and update registry.json")
    sync_parser.add_argument("--coord-root", type=Path, required=True, help="Coordination directory")
    sync_parser.add_argument("--workers-root", type=Path, required=True, help="Local worker directory")
    sync_parser.add_argument(
        "--scan-root",
        type=Path,
        action="append",
        default=[],
        help="Additional roots that may contain project worker bodies",
    )
    sync_parser.add_argument("--registry-path", type=Path, default=None, help="Optional explicit registry path")

    snapshot_parser = subparsers.add_parser(
        "snapshot-profiles",
        help="Generate _agent_profile snapshots for discovered workers",
    )
    snapshot_parser.add_argument("--coord-root", type=Path, required=True, help="Coordination directory")
    snapshot_parser.add_argument("--workers-root", type=Path, required=True, help="Local worker directory")
    snapshot_parser.add_argument(
        "--scan-root",
        type=Path,
        action="append",
        default=[],
        help="Additional roots that may contain project worker bodies",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "sync-registry":
        payload = sync_registry(
            coordination_root=args.coord_root,
            workers_root=args.workers_root,
            scan_roots=args.scan_root,
            registry_path=args.registry_path,
        )
        print(f"Synced registry with {len(payload['workers'])} workers.")
        return

    if args.command == "snapshot-profiles":
        written = snapshot_profiles(
            workers_root=args.workers_root,
            scan_roots=args.scan_root,
            coordination_root=args.coord_root,
        )
        print(f"Wrote {len(written)} profile snapshots.")
        return

    parser.error("Unknown command")


if __name__ == "__main__":
    main()
