from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent_control_plane.registry import sync_registry


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class RegistryTests(unittest.TestCase):
    def test_sync_registry_discovers_local_and_project_workers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            coordination = root / "coordination"
            workers_root = root / "workers"
            projects_root = root / "projects"

            write_json(coordination / "registry.json", {"controller": {"id": "controller"}, "workers": []})

            local_worker = workers_root / "profile-manager"
            write_json(
                local_worker / "worker-profile.json",
                {
                    "worker_id": "worker-profile-manager",
                    "alias": "Profile Manager",
                    "assistant_code": "B_profile_manager",
                    "assistant_level": "B",
                    "project_root": "..",
                    "agent_root": ".",
                    "status": "registered"
                },
            )

            project_worker = projects_root / "demo-project" / "_agent"
            write_json(
                project_worker / "worker-profile.json",
                {
                    "worker_id": "worker-demo",
                    "alias": "Demo Project Worker",
                    "assistant_code": "B_demo_project",
                    "assistant_level": "B",
                    "project_root": "..",
                    "agent_root": ".",
                    "status": "registered"
                },
            )

            payload = sync_registry(
                coordination_root=coordination,
                workers_root=workers_root,
                scan_roots=[projects_root],
            )

            self.assertEqual(len(payload["workers"]), 2)
            by_id = {worker["id"]: worker for worker in payload["workers"]}
            self.assertEqual(by_id["worker-profile-manager"]["background_worker"]["mode"], "daemon")
            self.assertEqual(by_id["worker-demo"]["background_worker"]["mode"], "ondemand")


if __name__ == "__main__":
    unittest.main()
