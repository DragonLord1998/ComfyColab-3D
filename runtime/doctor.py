#!/usr/bin/env python3
"""Offline structural doctor for the ComfyColab 3D pack."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NODE_FILE = ROOT / "custom_nodes" / "ComfyColab-3D" / "nodes.py"
PUBLIC_NODE_IDS = (
    "ComfyColabTrellisImageTo3D",
    "ComfyColabTrellis2MV",
    "ComfyColabUltraShapeRefine",
    "ComfyColabPixal3DImageTo3D",
    "ComfyColabPixal3DMV",
    "ComfyColabSkinTokensAutoRig",
    "ComfyColabCubePartSegment",
)
REQUIRED_PATHS = (
    NODE_FILE,
    ROOT / "worker" / "ultrashape" / "worker_main.py",
    ROOT / "worker" / "pixal3d" / "worker_main.py",
    ROOT / "worker" / "skintokens" / "worker_main.py",
    ROOT / "worker" / "cubepart" / "worker_main.py",
)


def doctor() -> dict[str, object]:
    missing_paths = [str(path.relative_to(ROOT)) for path in REQUIRED_PATHS if not path.is_file()]
    source = NODE_FILE.read_text(encoding="utf-8") if NODE_FILE.is_file() else ""
    missing_nodes = [node_id for node_id in PUBLIC_NODE_IDS if f'"{node_id}"' not in source]
    return {
        "schema": 1,
        "pack": "3d",
        "status": "ok" if not missing_paths and not missing_nodes else "error",
        "public_node_ids": list(PUBLIC_NODE_IDS),
        "missing_paths": missing_paths,
        "missing_node_ids": missing_nodes,
        "network_used": False,
        "writes": [],
    }


def main() -> int:
    result = doctor()
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
