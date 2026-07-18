# Contributing to ComfyColab 3D

## Scope

This repository owns mesh generation and refinement, multiview reconstruction,
rigging, part decomposition, its ComfyUI facade nodes, isolated workers,
workflows, dependency pins, patches, and 3D-specific validation. Generic Colab
installation and orchestration belong in ComfyColab core. Gaussian splats
belong in ComfyColab 3DGS.

Preserve the public node IDs and the legacy `ComfyColab-3D` target directory
unless a separately reviewed compatibility migration explicitly changes them.

## Local validation

Run the complete local suite before submitting a change:

```bash
PYTHON=/path/to/python3 bash scripts/check.sh
```

This proves manifest and file integrity, deterministic CPU-side behavior,
workflow wiring, worker protocols, and offline doctor behavior. It does not
prove CUDA compatibility, model download success, inference quality, VRAM use,
or performance on Colab.

## Live validation

Changes that affect GPU dependencies, cache profiles, patches, workers,
inference graphs, or output contracts also require a run on the pinned
Colab/GPU environment using `scripts/live_3d_g4_validation.py`. Store the
result in the documented validation record and report local and live outcomes
separately. A missing live run is an explicit release gap, not a local failure.

## Dependency and patch changes

- Pin Git and Hugging Face sources to immutable revisions.
- Verify artifact checksums before promotion.
- Keep heavyweight models lazy and installation dependencies declarative.
- Update third-party notices and license gates when ownership changes.
- Apply patches only to their declared source revision and content hashes.

## Pull-request checklist

- Manifest and project versions match.
- Public node and workflow compatibility is preserved or documented.
- `scripts/check.sh` passes.
- Local and live evidence are labeled separately.
- Changelog and notices reflect user-visible or dependency changes.
