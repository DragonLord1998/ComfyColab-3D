"""
@author: DragonLord1998
@title: ComfyColab 3D
@nickname: ComfyColab 3D
@description: Standalone image-to-3D, multiview, refinement, rigging, and segmentation nodes.
"""

from __future__ import annotations

import importlib
import importlib.util
import inspect
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def _set_default(name: str, value: Path) -> None:
    os.environ.setdefault(name, str(value))


def _configure_standalone_paths() -> None:
    standalone = ROOT / ".standalone"
    _set_default("COMFYCOLAB_3D_CACHE", ROOT / ".cache" / "comfycolab" / "3d")
    _set_default(
        "COMFYCOLAB_ULTRASHAPE_SOURCE",
        standalone / "sources" / "UltraShape-1.0",
    )
    _set_default(
        "COMFYCOLAB_PIXAL3D_SOURCE",
        standalone / "sources" / "Pixal3D",
    )
    _set_default(
        "COMFYCOLAB_SKINTOKENS_SOURCE",
        standalone / "sources" / "SkinTokens",
    )
    _set_default(
        "COMFYCOLAB_CUBEPART_SOURCE",
        standalone / "sources" / "cube" / "cubepart",
    )
    _set_default(
        "COMFYCOLAB_3D_MODEL_ROOT",
        standalone / "models" / "3d",
    )
    try:
        folder_paths = importlib.import_module("folder_paths")
        output_root = Path(folder_paths.get_output_directory()) / "3d"
    except (AttributeError, ModuleNotFoundError):
        output_root = standalone / "output" / "3d"
    _set_default("COMFYCOLAB_3D_OUTPUT", output_root)


def _load_internal_package():
    name = f"{__name__}._nodes"
    existing = sys.modules.get(name)
    if existing is not None:
        return existing
    package_dir = ROOT / "custom_nodes" / "ComfyColab-3D"
    spec = importlib.util.spec_from_file_location(
        name,
        package_dir / "__init__.py",
        submodule_search_locations=[str(package_dir)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load internal node package: {package_dir}")
    package = importlib.util.module_from_spec(spec)
    sys.modules[name] = package
    try:
        spec.loader.exec_module(package)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return package


async def comfy_entrypoint():
    _configure_standalone_paths()
    package = _load_internal_package()
    extension = package.comfy_entrypoint()
    if inspect.isawaitable(extension):
        extension = await extension
    return extension


__all__ = ["comfy_entrypoint"]
