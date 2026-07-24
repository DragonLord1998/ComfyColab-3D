# Changelog

All notable changes to ComfyColab 3D are recorded here. This project uses
semantic pre-release versions until the extracted pack has completed its live
GPU release gates.

## Unreleased

- Added a root ComfyUI V3 entrypoint, Manager metadata, node catalog, and
  standalone installer for the pinned TRELLIS2/GeometryPack base runtime.
- Added portable cache/model/output defaults that do not assume `/content`.
- Added standalone discovery and lifecycle diagnostics for all eight public
  node IDs.
- Added the pinned TRELLIS upstream environment lifecycle step and a
  checksum-bound current-ComfyUI dependency patch so isolated metadata scans
  include `comfy-kitchen`.
- Existing sibling dependencies must match their audited revisions before the
  installer reports success.
- Completed a live G4 TRELLIS image-to-3D run on stock ComfyUI 0.28.0,
  producing a textured volumetric GLB with 43,372 vertices and 48,014 faces.
- Pending: verify cache restoration and cold-install behavior through the
  modular ComfyColab core.
- Pending: add the generic `comfycolab-environment-toml` installer contract
  required by Pixal3D.

## 0.2.0-dev.0 - 2026-07-19

### Added

- Added the public `ComfyColabPixal3DMVAdvanced` workflow and VGGT-Omega
  depth/confidence-guided multiview adapter.
- Added pinned official VGGT-Omega source/model metadata plus a checksum-bound
  public retrieval fallback.

### Fixed

- Updated Pixal3D/CubePart artifact handling and the Pixal3D isolated worker
  environment.
- Hardened SkinTokens GLB validation, retry behavior, Blender export, and
  isolated worker metadata.

### Validation

- Recorded real Colab G4 evidence for Advanced Pixal3D MV and SkinTokens
  auto-rig while keeping unrelated pending gates explicit.

## 0.1.0-dev.0 - 2026-07-18

### Added

- Extracted the seven existing public 3D nodes without renaming their IDs,
  categories, schemas, or legacy `ComfyColab-3D` installation directory.
- Moved mesh workflows, isolated workers, cache profiles, content-addressed
  patches, dependency pins, notices, and validation tooling into this pack.
- Added the standalone `comfycolab-pack.json` contract and offline lifecycle
  hooks.

### Validation

- Local contract, graph, workflow, worker-protocol, geometry, cache, and
  artifact tests are available through `scripts/check.sh`.
- Live inference, VRAM, performance, and output-quality results remain a
  separate Colab/GPU gate and are not implied by local test success.
