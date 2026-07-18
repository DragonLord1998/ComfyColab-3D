from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "comfycolab-pack.json"
COMMIT = re.compile(r"^[0-9a-f]{40}$")
PUBLIC_NODE_IDS = {
    "ComfyColabTrellisImageTo3D",
    "ComfyColabTrellis2MV",
    "ComfyColabUltraShapeRefine",
    "ComfyColabPixal3DImageTo3D",
    "ComfyColabPixal3DMV",
    "ComfyColabSkinTokensAutoRig",
    "ComfyColabCubePartSegment",
}


class PackContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_identity_and_legacy_node_root_are_stable(self) -> None:
        self.assertEqual(self.manifest["schema"], 1)
        self.assertEqual(self.manifest["id"], "3d")
        self.assertEqual(
            self.manifest["node_roots"],
            [{"source": "custom_nodes/ComfyColab-3D", "target": "ComfyColab-3D"}],
        )

    def test_release_hygiene_is_explicitly_prerelease(self) -> None:
        version = self.manifest["version"]
        self.assertRegex(version, r"^\d+\.\d+\.\d+-dev\.\d+$")
        project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn(f'version = "{version}"', project)
        self.assertTrue((ROOT / "CHANGELOG.md").is_file())
        self.assertTrue((ROOT / "CONTRIBUTING.md").is_file())

    def test_public_node_inventory_matches_manifest(self) -> None:
        self.assertEqual(set(self.manifest["health_checks"]["node_ids"]), PUBLIC_NODE_IDS)
        source = (ROOT / "custom_nodes/ComfyColab-3D/nodes.py").read_text(encoding="utf-8")
        for node_id in PUBLIC_NODE_IDS:
            self.assertIn(f'"{node_id}"', source)

    def test_dependency_refs_are_immutable_and_destinations_are_unique(self) -> None:
        dependencies = self.manifest["dependencies"]
        destinations = [dependency["destination"] for dependency in dependencies]
        self.assertEqual(len(destinations), len(set(destinations)))
        for dependency in dependencies:
            self.assertIn(dependency["install_phase"], {"bootstrap", "lazy"})
            if dependency["kind"] in {"git", "huggingface"}:
                self.assertRegex(dependency["ref"], COMMIT)
            if dependency["kind"] == "artifact":
                self.assertRegex(dependency["sha256"], r"^[0-9a-f]{64}$")
            if dependency["kind"] in {"huggingface", "artifact"}:
                self.assertEqual(dependency["install_phase"], "lazy")

    def test_patch_files_match_declared_digests_and_source_refs(self) -> None:
        dependency_refs = {
            dependency["id"]: dependency.get("ref")
            for dependency in self.manifest["dependencies"]
        }
        for patch in self.manifest["patches"]:
            path = ROOT / patch["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), patch["sha256"])
            self.assertEqual(patch["source_ref"], dependency_refs[patch["target"]])

    def test_hooks_and_workflows_exist(self) -> None:
        for hook in self.manifest["hooks"].values():
            self.assertEqual(hook["network"], "none")
            self.assertTrue((ROOT / hook["path"]).is_file())
        for workflow in self.manifest["workflows"]:
            payload = json.loads((ROOT / workflow).read_text(encoding="utf-8"))
            self.assertIn("nodes", payload)
            self.assertIn("links", payload)

    def test_3dgs_runtime_logic_is_not_owned_by_mesh_pack(self) -> None:
        production = [
            ROOT / "custom_nodes",
            ROOT / "worker",
            ROOT / "runtime",
            ROOT / "scripts",
        ]
        offenders = []
        for directory in production:
            for path in directory.rglob("*"):
                if path.is_file() and path.suffix in {".py", ".json"}:
                    text = path.read_text(encoding="utf-8", errors="ignore").lower()
                    if "triposplat" in text or "gaussiansplat" in text:
                        offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_pack_sources_do_not_import_comfycolab_core(self) -> None:
        production = [
            ROOT / "custom_nodes",
            ROOT / "worker",
            ROOT / "runtime",
            ROOT / "scripts",
        ]
        for directory in production:
            for path in directory.rglob("*.py"):
                content = path.read_text(encoding="utf-8")
                self.assertNotIn("from comfycolab", content, path)
                self.assertNotIn("import comfycolab", content, path)


if __name__ == "__main__":
    unittest.main()
