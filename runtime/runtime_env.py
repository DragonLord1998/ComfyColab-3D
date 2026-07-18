#!/usr/bin/env python3
"""Emit 3D pack environment contributions from resolver-owned paths."""

from __future__ import annotations

import json
import sys


def main() -> int:
    raw_context = sys.stdin.read()
    context = json.loads(raw_context) if raw_context.strip() else {}
    paths = context.get("resolved_paths", {})
    environment = {
        "COMFYCOLAB_ULTRASHAPE_SOURCE": paths.get("ultrashape-source", "/content/UltraShape-1.0"),
        "COMFYCOLAB_PIXAL3D_SOURCE": paths.get("pixal3d-source", "/content/Pixal3D"),
        "COMFYCOLAB_SKINTOKENS_SOURCE": paths.get("skintokens-source", "/content/SkinTokens"),
        "COMFYCOLAB_CUBEPART_SOURCE": paths.get("cubepart-source", "/content/cube/cubepart"),
    }
    print(json.dumps({"schema": 1, "pack": "3d", "environment": environment}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
