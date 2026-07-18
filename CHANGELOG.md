# Changelog

All notable changes to ComfyColab 3D are recorded here. This project uses
semantic pre-release versions until the extracted pack has completed its live
GPU release gates.

## Unreleased

- Pending: execute and publish the pinned Colab/G4 live-validation record.
- Pending: verify cache restoration and cold-install behavior through the
  modular ComfyColab core.
- Pending: add the generic `comfycolab-environment-toml` installer contract
  required by Pixal3D.

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
