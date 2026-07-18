# ComfyColab 3D validation

This repository keeps mesh/GLB validation separate from the Gaussian-splat
validation owned by `ComfyColab-3DGS`.

## Local contract gates

The pack-local check covers:

- the seven preserved public node IDs and saved workflow filenames;
- native `FILE_3D_GLB` contracts and geometry-quality checks;
- TRELLIS and UltraShape graph expansion;
- Pixal3D, SkinTokens, CubePart, and UltraShape worker protocols;
- cache, refresh, cancellation, artifact integrity, and license gates;
- revision-bound patches and cache manifests;
- manifest, hook, dependency, and repository-boundary conformance.

Run:

```bash
PYTHON=/path/to/python3 bash scripts/check.sh
```

## Live G4 boundary

Local success does not prove model inference, memory use, output quality, or
cache portability. `scripts/live_3d_g4_validation.py` records those separately.
The machine-readable state in `3d-validation.json` remains pending unless a
real pinned Colab G4 run produces the required GLB evidence.

Existing proof for the strict 1536 no-downgrade path and combined CUDA probes is
retained. Model-specific gates that have not completed end to end remain
pending, including TRELLIS 512/1024/1536, multiview, UltraShape, Pixal3D,
SkinTokens, CubePart, full-workflow, cache-hit, cancellation, and native
Preview3D/SaveGLB paths.

## Cache publication

`scripts/build_3d_cache.py` may package the combined environment only after its
required live gates and benchmarks are recorded as passed. It does not publish
release assets. Existing `trellis2-cache-v1` URLs must remain available as the
rollback source even after new cache generations move to this repository.

