"""Pack-owned runtime adapter used by the 3D cache builder."""

from __future__ import annotations

import os
import platform
import posixpath
import subprocess
import sys
from pathlib import Path, PurePosixPath

from .pins import *  # Re-export the immutable compatibility surface.


ROOT = Path(__file__).resolve().parents[1]


def trellis_cache_compatible() -> bool:
    if platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"}:
        return False
    if sys.version_info[:3] != (3, 12, 13) or platform.libc_ver() != ("glibc", "2.35"):
        return False
    try:
        import torch
    except ImportError:
        return False
    return (
        torch.__version__ == "2.11.0+cu128"
        and (torch.version.cuda or "") == "12.8"
        and torch.cuda.is_available()
        and "RTX PRO 6000" in torch.cuda.get_device_name(0).upper()
        and torch.cuda.get_device_capability(0) == (12, 0)
    )


def _safe_cache_member(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(
        path.parts
        and not path.is_absolute()
        and ".." not in path.parts
        and path.parts[0] == ".ce"
    )


def validate_trellis_archive(archive: Path) -> None:
    result = subprocess.run(
        ["tar", "--zstd", "-tvf", str(archive)],
        check=True,
        text=True,
        capture_output=True,
        timeout=180,
    )
    entries = result.stdout.splitlines()
    if not entries:
        raise RuntimeError("The 3D cache archive is empty.")
    for entry in entries:
        fields = entry.split(maxsplit=5)
        if len(fields) != 6:
            raise RuntimeError(f"Malformed 3D cache archive entry: {entry}")
        kind = entry[0]
        details = fields[5]
        if kind == "l":
            if " -> " not in details:
                raise RuntimeError(f"Malformed 3D cache symlink: {entry}")
            member, target = details.rsplit(" -> ", 1)
        elif kind == "h":
            if " link to " not in details:
                raise RuntimeError(f"Malformed 3D cache hard link: {entry}")
            member, target = details.rsplit(" link to ", 1)
        elif kind in {"-", "d"}:
            member, target = details, None
        else:
            raise RuntimeError(f"Unsupported 3D cache archive entry: {entry}")
        if not _safe_cache_member(member):
            raise RuntimeError(f"Unsafe 3D cache archive member: {member}")
        if target is None:
            continue
        target_path = PurePosixPath(target)
        if target_path.is_absolute():
            final_root = PurePosixPath("/root/.ce")
            if target_path != final_root and final_root not in target_path.parents:
                raise RuntimeError(f"Unsafe 3D cache link target: {target}")
        elif kind == "h":
            if not _safe_cache_member(target):
                raise RuntimeError(f"Unsafe 3D cache hard-link target: {target}")
        else:
            resolved = posixpath.normpath(
                posixpath.join(posixpath.dirname(member), target)
            )
            if not _safe_cache_member(resolved):
                raise RuntimeError(f"Unsafe 3D cache symlink target: {target}")


def _run_probe(python: Path, source: str, *, cwd: Path | None = None) -> None:
    if not python.is_file():
        raise RuntimeError(f"Required cached Python is missing: {python}")
    subprocess.run(
        [str(python), "-c", source],
        cwd=cwd,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
    )


def validate_trellis_cache(
    workspace: Path,
    *,
    validate_ultrashape: bool = False,
) -> None:
    envs = workspace / ".pixi" / "envs"
    _run_probe(
        envs / "trellis2-nodes" / "bin" / "python",
        "import torch, cumesh_vb, drtk, flash_attn, flex_gemm_ap, "
        "o_voxel_vb_ap, sageattention; "
        "assert torch.__version__ == '2.11.0+cu128'; "
        "assert torch.version.cuda == '12.8'; "
        "assert torch.cuda.get_device_capability() == (12, 0); "
        "x = torch.ones(4, device='cuda'); torch.cuda.synchronize(); "
        "assert x.sum().item() == 4.0",
    )
    _run_probe(
        envs / "geometrypack-nodes" / "bin" / "python",
        "import torch, cumesh; "
        "assert torch.__version__ == '2.11.0+cu128'; "
        "assert torch.version.cuda == '12.8'; "
        "assert torch.cuda.get_device_capability() == (12, 0); "
        "x = torch.ones(4, device='cuda'); torch.cuda.synchronize(); "
        "assert x.sum().item() == 4.0",
    )
    if validate_ultrashape:
        source_root = Path(
            os.environ.get("COMFYCOLAB_ULTRASHAPE_SOURCE", "/content/UltraShape-1.0")
        )
        _run_probe(
            envs / "trellis2-nodes" / "bin" / "python",
            "import torch, cubvh; "
            "from ultrashape.pipelines import UltraShapePipeline; "
            "from ultrashape.surface_loaders import SharpEdgeSurfaceLoader; "
            "assert torch.cuda.get_device_capability() == (12, 0)",
            cwd=source_root,
        )


def install_ultrashape_overlay() -> None:
    python = Path.home() / ".ce" / ".pixi" / "envs" / "trellis2-nodes" / "bin" / "python"
    requirements = ROOT / "worker" / "ultrashape" / "requirements-inference.txt"
    subprocess.run(
        [str(python), "-m", "pip", "install", "-r", str(requirements)],
        check=True,
    )
    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--no-build-isolation",
            f"git+https://github.com/ashawkey/cubvh.git@{ULTRASHAPE_CUBVH_REF}",
        ],
        check=True,
    )
    validate_trellis_cache(Path.home() / ".ce", validate_ultrashape=True)

