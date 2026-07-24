from __future__ import annotations

import asyncio
import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path

from tests.test_3d_node_pack import FakeIO, GraphBuilder


ROOT = Path(__file__).resolve().parents[1]


def load_root_package():
    name = "normalized_3d_manager_name"
    for module_name in list(sys.modules):
        if module_name == name or module_name.startswith(name + "."):
            del sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(
        name,
        ROOT / "__init__.py",
        submodule_search_locations=[str(ROOT)],
    )
    package = importlib.util.module_from_spec(spec)
    sys.modules[name] = package
    assert spec.loader
    spec.loader.exec_module(package)
    return package


class StandaloneLoadingTests(unittest.TestCase):
    def setUp(self):
        names = (
            "comfy_api",
            "comfy_api.latest",
            "comfy_execution",
            "comfy_execution.graph_utils",
        )
        self.saved_modules = {name: sys.modules.get(name) for name in names}
        latest = types.ModuleType("comfy_api.latest")
        latest.io = FakeIO
        latest.Types = types.SimpleNamespace(
            File3D=lambda path, file_format: (path, file_format)
        )
        latest.ComfyExtension = type("ComfyExtension", (), {})
        api = types.ModuleType("comfy_api")
        api.latest = latest
        execution = types.ModuleType("comfy_execution")
        graph_utils = types.ModuleType("comfy_execution.graph_utils")
        graph_utils.GraphBuilder = GraphBuilder
        sys.modules.update(
            {
                "comfy_api": api,
                "comfy_api.latest": latest,
                "comfy_execution": execution,
                "comfy_execution.graph_utils": graph_utils,
            }
        )

    def tearDown(self):
        for name, module in self.saved_modules.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module

    def test_root_discovers_all_public_nodes_from_any_folder_name(self):
        package = load_root_package()
        extension = asyncio.run(package.comfy_entrypoint())
        node_classes = asyncio.run(extension.get_node_list())
        public_ids = {
            node.define_schema().node_id
            for node in node_classes
            if not getattr(node.define_schema(), "is_dev_only", False)
        }
        declared = set(
            json.loads((ROOT / "node_list.json").read_text(encoding="utf-8"))
        )
        self.assertEqual(public_ids, declared)

    def test_manager_files_and_pinned_dependencies_are_present(self):
        self.assertTrue((ROOT / "requirements.txt").is_file())
        self.assertTrue((ROOT / "install.py").is_file())
        installer = (ROOT / "install.py").read_text(encoding="utf-8")
        self.assertIn("9b878516f2dc2fd873f4f6cceadba403dd12d83e", installer)
        self.assertIn("c67199de05705642258e727fa118f412877b4ebf", installer)
        self.assertIn("trellis2-current-comfy-runtime.json", installer)
        self.assertIn("_run_pinned_installer(trellis, DEPENDENCIES[0][2])", installer)
        self.assertIn('_run(sys.executable, "install.py", cwd=repository)', installer)
        self.assertIn("and _commit(custom_nodes / name) == revision", installer)


if __name__ == "__main__":
    unittest.main()
