# Third-party notices

This pack downloads and connects third-party projects at runtime. It does not
store their model weights in this Git repository. Upstream license files and
terms control.

## TRELLIS.2 and ComfyUI integrations

- ComfyUI wrapper: <https://github.com/PozzettiAndrea/ComfyUI-TRELLIS2>
- Pinned wrapper revision: `9b878516f2dc2fd873f4f6cceadba403dd12d83e`
- GeometryPack: <https://github.com/PozzettiAndrea/ComfyUI-GeometryPack>
- Pinned GeometryPack revision: `c67199de05705642258e727fa118f412877b4ebf`
- TRELLIS.2 model: <https://huggingface.co/microsoft/TRELLIS.2-4B>
- BiRefNet revision: `e2bf8e4460fc8fa32bba5ea4d94b3233d367b0e4`

The wrapper, model, conditioning-model, and transitive CUDA/package licenses
remain applicable. The public TRELLIS2MV facade uses the wrapper's multiview
node; the revision-checked cache patch does not alter its view blending math.

## UltraShape 1.0

- Source revision: `5e8dcef05df101ab00ab6cd5fdd0ed0c74fbca66`
- Model revision: `5aeb21a7185d39f042d02b2695802f125a6f5159`
- DINOv2 Large revision: `47b73eefe95e8d44ec3623f8890bd894b6ea2d6c`
- cubvh revision: `757b913bfbf19ed65e3a379d159391a8e29efa0f`

The pinned source includes the Tencent Hunyuan 3D 2.1 Community License and
acceptable-use terms, including territory and hosted-service restrictions.
The model repository separately declares Apache-2.0 metadata. The pack applies
only revision-checked inference compatibility patches.

## Pixal3D

- Source revision: `cdbb2bbffbf4e6f298b5f2af3d1d76a8d823d2af`
- Model revision: `0b31f9160aa400719af409098bff7936a932f726`
- DINOv3 revision: `3c276edd87d6f6e569ff0c4400e086807d0f3881`
- MoGe model revision: `39c4d5e957afe587e04eec59dc2bcc3be5ecd968`
- MoGe source revision: `07444410f1e33f402353b99d6ccd26bd31e469e8`
- NAF revision: `37f2dfc180f2de53d98bd601109c0da0dd6b0f43`

Pixal3D is installed in an isolated worker environment. Review all project,
model, package, access, and regional terms before commercial or hosted use.
Pixal3DMV is an experimental ComfyColab adapter, not an official Pixal3D mode.

The separate Advanced Pixal3DMV adapter optionally uses VGGT-Omega:

- Official source: <https://github.com/facebookresearch/vggt-omega>
- Pinned source revision: `39a0cb8af88554f15ddcb5354cd52bde588fa014`
- Official model: <https://huggingface.co/facebook/VGGT-Omega>
- Pinned model revision: `05654241adc2f218dfb089c373a011f8a7040576`
- Public fallback mirror: <https://huggingface.co/1kaiser/vggt-omega-jax>
- Pinned fallback revision: `a8c3a718e0cf78e9e4c6847229efea793d37f060`
- Required checkpoint SHA-256: `c02da418b18bb01d0392598d3f6147366bcde1bb70fd08a5e3bf7925b0667934`

The source uses the FAIR Noncommercial Research License v1. The official model
is labeled CC BY-NC 4.0 and remains access-gated. ComfyColab does not redistribute VGGT-Ω source or weights. The fallback is only a retrieval path:
its checkpoint must match the official byte size and SHA-256, and its
availability is not a grant of rights or official access approval.

## SkinTokens / TokenRig

- Source revision: `273b691d35989d71cd17ff2895fdc735097b92d1`
- Model revision: `79736cad0fd84de384d5eede659b4ebd24effe33`
- Qwen3-0.6B revision: `c1899de289a04d12100db370d81485cdf75e47ca`
- Declared source/model metadata: MIT

The isolated runtime also invokes Blender for GLB skin export and carries its
transitive CUDA, FlashAttention, and package licenses.

## CubePart

- Source revision: `3c6d06ddbef3160a1e1950cb13ab63dd12a61e50`
- Model revision: `28431d124e77040fcaf34c0a71623ff61d35a6c0`
- Code terms: Cube3D Research-Only RAIL-MS
- Model metadata: OpenRAIL, subject to the upstream repository terms

CubePart is disabled until `accept_research_license` is explicitly enabled.
This pack does not convert its research-only terms into a commercial license.
