# ComfyColab 3D

`ComfyColab-3D` is the independently versioned mesh/asset pack for
[ComfyColab](https://github.com/DragonLord1998/ComfyColab). It owns mesh
generation and refinement, multiview reconstruction, rigging, part
decomposition, GLB contracts, isolated workers, cache profiles, patches,
workflows, tests, and validation records.

The pack preserves the legacy ComfyUI target
directory `ComfyColab-3D`, all eight public node IDs, their categories and
schemas, and the existing workflow filenames.

## Development status

The current version is `0.2.0-dev.0`. It is a development pre-release: the
pack boundary and local contracts are testable, but it is not a stable release
claim and does not imply that every live GPU gate has passed.

## Public nodes

- `ComfyColabTrellisImageTo3D`
- `ComfyColabTrellis2MV`
- `ComfyColabUltraShapeRefine`
- `ComfyColabPixal3DImageTo3D`
- `ComfyColabPixal3DMV`
- `ComfyColabPixal3DMVAdvanced`
- `ComfyColabSkinTokensAutoRig`
- `ComfyColabCubePartSegment`

The pack also contains dev-only adapter nodes used by expanded workflows. They
remain internal and are not presented as additional public capabilities.

## Layout

- `comfycolab-pack.json` — immutable dependency, patch, workflow, and health contract
- `custom_nodes/ComfyColab-3D/` — legacy-compatible ComfyUI node pack
- `worker/` — UltraShape, Pixal3D, SkinTokens, and CubePart runtimes
- `patches/` and `cache/` — revision-bound runtime assets
- `workflows/` — saved public workflows
- `scripts/` — validation and cache-build tools
- `docs/` — local/live validation records

## Validation tiers

Local validation is the required first tier:

```bash
python3 -m pip install -e ".[test]"
PYTHON=/path/to/python3 bash scripts/check.sh
```

The test extra enables NumPy- and Pillow-backed cases; without it those
dependency-specific tests are reported as optional skips. Local checks validate
contracts and deterministic CPU-side behavior. They do not claim that pending
Colab G4 inference, VRAM, performance, or output-quality gates have passed.

The generic core still rejects this development manifest because Pixal3D uses
the not-yet-supported `comfycolab-environment-toml` installer and the four
isolated workers do not yet have a generic cache-restore contract. The local
suite therefore proves the extracted pack boundary, not runtime installability.

Live validation is a separate, environment-specific tier. It must run on the
pinned Colab/GPU stack and record real inference artifacts and metrics through
`scripts/live_3d_g4_validation.py`. See `docs/3d-validation.md`; never promote a
local pass into a live-pass claim.

CubePart remains disabled until the user explicitly accepts its research-only
terms. See `THIRD_PARTY_NOTICES.md`.
