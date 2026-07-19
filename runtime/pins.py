"""Immutable 3D source, model, patch, and environment pins."""

from __future__ import annotations


COMFY_REF = "8b099de36acd81acd1afa3b5442951dc847e0a52"
TRELLIS_REF = "9b878516f2dc2fd873f4f6cceadba403dd12d83e"
GEOMETRY_REF = "c67199de05705642258e727fa118f412877b4ebf"
ULTRASHAPE_REF = "5e8dcef05df101ab00ab6cd5fdd0ed0c74fbca66"
ULTRASHAPE_CUBVH_REF = "757b913bfbf19ed65e3a379d159391a8e29efa0f"
BIREFNET_MODEL_REF = "e2bf8e4460fc8fa32bba5ea4d94b3233d367b0e4"
PIXAL3D_REF = "cdbb2bbffbf4e6f298b5f2af3d1d76a8d823d2af"
PIXAL3D_MODEL_REPO = "TencentARC/Pixal3D"
PIXAL3D_MODEL_REF = "0b31f9160aa400719af409098bff7936a932f726"
PIXAL3D_DINOV3_MODEL_REPO = "camenduru/dinov3-vitl16-pretrain-lvd1689m"
PIXAL3D_DINOV3_MODEL_REF = "3c276edd87d6f6e569ff0c4400e086807d0f3881"
PIXAL3D_MOGE_MODEL_REPO = "Ruicheng/moge-2-vitl"
PIXAL3D_MOGE_MODEL_REF = "39c4d5e957afe587e04eec59dc2bcc3be5ecd968"
PIXAL3D_MOGE_SOURCE_REF = "07444410f1e33f402353b99d6ccd26bd31e469e8"
PIXAL3D_NAF_REPO = "valeoai/NAF"
PIXAL3D_NAF_REF = "37f2dfc180f2de53d98bd601109c0da0dd6b0f43"
PIXAL3D_NAF_CHECKPOINT_SHA256 = (
    "c096c1ab2217a5c3ac136365f721685e2201379cb69d509cfb0261183847c98f"
)
PIXAL3D_UTILS3D_WHEEL = (
    "https://github.com/LDYang694/Storages/releases/download/"
    "20260430/utils3d-0.0.2-py3-none-any.whl"
)
PIXAL3D_NATTEN_PACKAGE = "natten==0.21.6+torch2110cu128"
PIXAL3D_NVDIFFRAST_REF = "253ac4fcea7de5f396371124af597e6cc957bfae"
PIXAL3D_VGGT_OMEGA_SOURCE_REF = "39a0cb8af88554f15ddcb5354cd52bde588fa014"
PIXAL3D_VGGT_OMEGA_MODEL_REF = "05654241adc2f218dfb089c373a011f8a7040576"
PIXAL3D_VGGT_OMEGA_FALLBACK_MODEL_REF = "a8c3a718e0cf78e9e4c6847229efea793d37f060"
PIXAL3D_VGGT_OMEGA_FALLBACK_CHECKPOINT_URL = (
    "https://huggingface.co/1kaiser/vggt-omega-jax/resolve/"
    f"{PIXAL3D_VGGT_OMEGA_FALLBACK_MODEL_REF}/"
    "vggt_omega_1b_512.pt?download=true"
)
PIXAL3D_VGGT_OMEGA_CHECKPOINT_SHA256 = (
    "c02da418b18bb01d0392598d3f6147366bcde1bb70fd08a5e3bf7925b0667934"
)
PIXAL3D_ENVIRONMENT_REF = "g4-linux64-py31213-torch2110-cu128-sm120-pixal3d-v3"
SKINTOKENS_REF = "273b691d35989d71cd17ff2895fdc735097b92d1"
SKINTOKENS_MODEL_REPO = "VAST-AI/SkinTokens"
SKINTOKENS_MODEL_REF = "79736cad0fd84de384d5eede659b4ebd24effe33"
SKINTOKENS_QWEN_REPO = "Qwen/Qwen3-0.6B"
SKINTOKENS_QWEN_REF = "c1899de289a04d12100db370d81485cdf75e47ca"
CUBEPART_REF = "3c6d06ddbef3160a1e1950cb13ab63dd12a61e50"
CUBEPART_MODEL_REPO = "Roblox/cubepart"
CUBEPART_MODEL_REF = "28431d124e77040fcaf34c0a71623ff61d35a6c0"
COMFY_ENV_VERSION = "0.3.89"

TRELLIS_PATCH_ID = "trellis2-strict-1536-birefnet-pin-metrics-v4"
TRELLIS_CATEGORY_PATCH_ID = "trellis2-advanced-categories-v1"
TRELLIS_MULTIVIEW_PATCH_ID = "trellis2-multiview-weight-cache-v1"
ULTRASHAPE_PATCH_ID = "ultrashape-inference-compat-v3"
PIXAL3D_PATCH_ID = "pixal3d-persistent-worker-v1"


def expected_pixal3d_sources() -> dict[str, str]:
    return {
        "pixal3d": PIXAL3D_REF,
        "pixal3dModel": PIXAL3D_MODEL_REF,
        "dinov3": PIXAL3D_DINOV3_MODEL_REF,
        "mogeModel": PIXAL3D_MOGE_MODEL_REF,
        "mogeSource": PIXAL3D_MOGE_SOURCE_REF,
        "naf": PIXAL3D_NAF_REF,
        "nafCheckpoint": PIXAL3D_NAF_CHECKPOINT_SHA256,
        "utils3d": PIXAL3D_UTILS3D_WHEEL,
        "natten": PIXAL3D_NATTEN_PACKAGE,
        "nvdiffrast": PIXAL3D_NVDIFFRAST_REF,
        "vggtOmega": PIXAL3D_VGGT_OMEGA_SOURCE_REF,
        "vggtOmegaModel": PIXAL3D_VGGT_OMEGA_MODEL_REF,
        "vggtOmegaFallbackModel": PIXAL3D_VGGT_OMEGA_FALLBACK_MODEL_REF,
        "vggtOmegaFallbackCheckpointUrl": (
            PIXAL3D_VGGT_OMEGA_FALLBACK_CHECKPOINT_URL
        ),
        "vggtOmegaCheckpointSha256": PIXAL3D_VGGT_OMEGA_CHECKPOINT_SHA256,
        "environment": PIXAL3D_ENVIRONMENT_REF,
        "comfyEnv": COMFY_ENV_VERSION,
    }
