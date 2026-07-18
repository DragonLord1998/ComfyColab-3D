#!/usr/bin/env python3
"""Validate the resolved 3D pack context without performing installation."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    raw_context = sys.stdin.read()
    context = json.loads(raw_context) if raw_context.strip() else {}
    lock = context.get("lock", {})
    result = {
        "schema": 1,
        "pack": "3d",
        "status": "configured",
        "pack_root": str(ROOT),
        "lock_digest": context.get("lock_digest"),
        "declared_dependencies": len(lock.get("dependencies", [])) if isinstance(lock, dict) else 0,
        "writes": [],
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
