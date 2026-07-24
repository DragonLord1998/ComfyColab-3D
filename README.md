# ComfyColab 3D

`ComfyColab-3D` is a standalone ComfyUI custom-node repository and the
independently versioned mesh/asset pack for
[ComfyColab](https://github.com/DragonLord1998/ComfyColab). It owns mesh
generation and refinement, multiview reconstruction, rigging, part
decomposition, GLB contracts, isolated workers, cache profiles, patches,
workflows, tests, and validation records.

The pack preserves the legacy ComfyUI target
directory `ComfyColab-3D`, all eight public node IDs, their categories and
schemas, and the existing workflow filenames.

## Development status

The current version is `0.3.0-dev.1`. It is a development pre-release: the
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

## Standalone installation

Install the Git repository through ComfyUI Manager, or install manually:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/DragonLord1998/ComfyColab-3D.git
cd ComfyColab-3D
python install.py
```

Use the Python executable that starts ComfyUI, then restart ComfyUI. The
installer adds exact pinned sibling checkouts of ComfyUI-TRELLIS2 and
ComfyUI-GeometryPack only when they are absent, installs their declared Python
requirements, and applies revision- and checksum-bound TRELLIS compatibility
patches before running the pinned TRELLIS isolated-environment installer.
Existing exact-pinned checkouts are reused; different or non-git installations
produce an actionable error and are never overwritten.

The base standalone install supports the public TRELLIS image-to-3D and
multiview facades. UltraShape, Pixal3D, SkinTokens, and CubePart remain visible
but use optional isolated worker environments. Their error messages identify
the missing environment instead of installing packages at ComfyUI runtime.
CubePart additionally remains disabled until its research-only terms are
explicitly accepted.

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

The managed ComfyColab core still rejects this development manifest because Pixal3D uses
the not-yet-supported `comfycolab-environment-toml` installer and the four
isolated workers do not yet have a generic cache-restore contract. The local
suite therefore proves the extracted pack boundary, not runtime installability.

Live validation is a separate, environment-specific tier. It must run on the
pinned Colab/GPU stack and record real inference artifacts and metrics through
`scripts/live_3d_g4_validation.py`. See `docs/3d-validation.md`; never promote a
local pass into a live-pass claim.

See `THIRD_PARTY_NOTICES.md` for optional dependency and license details.
