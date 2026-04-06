from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent_control_plane.snapshot import snapshot_profiles


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class SnapshotTests(unittest.TestCase):
    def test_snapshot_profiles_writes_portable_profile_layer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            coordination = root / "coordination"
            workers_root = root / "workers"
            worker_root = workers_root / "ops-manager"

            write_text(coordination / "governance.md", "# Governance\n")
            write_json(
                worker_root / "worker-profile.json",
                {
                    "worker_id": "worker-ops",
                    "alias": "Ops Manager",
                    "assistant_code": "B_ops_manager",
                    "assistant_level": "B",
                    "project_root": "..",
                    "agent_root": ".",
                    "staffing_standard_path": str((coordination / "governance.md").resolve())
                },
            )
            write_text(worker_root / "memory" / "session_memory.md", "# Session Memory\nKeep task scope explicit.\n")

            written = snapshot_profiles(
                workers_root=workers_root,
                scan_roots=[],
                coordination_root=coordination,
            )

            self.assertEqual(len(written), 1)
            snapshot_root = worker_root / "_agent_profile"
            self.assertTrue((snapshot_root / "README.md").exists())
            self.assertTrue((snapshot_root / "memory" / "session_memory_snapshot.md").exists())
            self.assertTrue((snapshot_root / "rules" / "rules_snapshot" / "governance.md").exists())


if __name__ == "__main__":
    unittest.main()
