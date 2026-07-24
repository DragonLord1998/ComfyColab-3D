#!/usr/bin/env python3
"""Install the base standalone ComfyUI dependencies for ComfyColab 3D."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
DEPENDENCIES = (
    (
        "ComfyUI-TRELLIS2",
        "https://github.com/PozzettiAndrea/ComfyUI-TRELLIS2.git",
        "9b878516f2dc2fd873f4f6cceadba403dd12d83e",
    ),
    (
        "ComfyUI-GeometryPack",
        "https://github.com/PozzettiAndrea/ComfyUI-GeometryPack.git",
        "c67199de05705642258e727fa118f412877b4ebf",
    ),
)
TRELLIS_PATCHES = (
    "trellis2-no-1536-downgrade.json",
    "trellis2-advanced-categories.json",
    "trellis2-multiview-weight-cache.json",
    "trellis2-current-comfy-runtime.json",
)


def _run(*argv: str, cwd: Path | None = None) -> None:
    subprocess.run(
        list(argv),
        cwd=str(cwd) if cwd else None,
        check=True,
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _commit(path: Path) -> str | None:
    if not (path / ".git").is_dir():
        return None
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _custom_nodes_root() -> Path:
    parent = ROOT.parent
    if parent.name != "custom_nodes":
        raise RuntimeError(
            "ComfyColab-3D must be directly inside ComfyUI/custom_nodes "
            "before install.py is run."
        )
    return parent


def _apply_patch(repository: Path, specification_path: Path) -> str:
    specification = json.loads(specification_path.read_text(encoding="utf-8"))
    patch_id = str(specification.get("patch_id", ""))
    expected_revision = str(specification.get("revision", ""))
    if specification.get("schema") != 1 or not patch_id or not expected_revision:
        raise RuntimeError(f"Invalid patch metadata: {specification_path}")
    if _commit(repository) != expected_revision:
        raise RuntimeError(
            f"Patch {patch_id} requires exact revision {expected_revision}"
        )

    root = repository.resolve()
    prepared: list[tuple[Path, str, int]] = []
    states: set[str] = set()
    for file_specification in specification.get("files", []):
        relative = PurePosixPath(str(file_specification.get("path", "")))
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError(f"Unsafe patch path: {relative}")
        path = (repository / Path(*relative.parts)).resolve()
        if path != root and root not in path.parents:
            raise RuntimeError(f"Patch escapes repository: {relative}")
        before_hash = str(file_specification.get("before_sha256", ""))
        after_hash = str(file_specification.get("after_sha256", ""))
        actual_hash = _sha256(path)
        if actual_hash == after_hash:
            states.add("after")
            continue
        if actual_hash != before_hash:
            raise RuntimeError(
                f"Patch {patch_id} refused unexpected content in {relative}"
            )
        states.add("before")
        content = path.read_text(encoding="utf-8")
        for replacement in file_specification.get("replacements", []):
            before = "\n".join(replacement["before_lines"]) + "\n"
            after = "\n".join(replacement["after_lines"])
            if replacement["after_lines"]:
                after += "\n"
            occurrences = int(replacement.get("occurrences", 1))
            if content.count(before) != occurrences:
                raise RuntimeError(
                    f"Patch {patch_id} found an unexpected match count in {relative}"
                )
            content = content.replace(before, after, occurrences)
        if hashlib.sha256(content.encode("utf-8")).hexdigest() != after_hash:
            raise RuntimeError(f"Patch {patch_id} produced an unexpected hash")
        prepared.append((path, content, path.stat().st_mode))
    if states == {"after"}:
        return patch_id
    if states != {"before"}:
        raise RuntimeError(f"Patch {patch_id} is partially applied")
    for path, content, mode in prepared:
        temporary = path.with_suffix(path.suffix + ".comfycolab-patch")
        temporary.write_text(content, encoding="utf-8")
        temporary.chmod(mode)
        temporary.replace(path)
    return patch_id


def _install_dependency(name: str, repository: str, revision: str) -> Path:
    target = _custom_nodes_root() / name
    if target.exists():
        actual = _commit(target)
        if actual != revision:
            raise RuntimeError(
                f"Existing {name} is not the audited revision required by "
                f"ComfyColab 3D. Expected {revision}, found "
                f"{actual or 'a non-git installation'}. Move or update that "
                "checkout explicitly, then rerun this installer."
            )
        print(
            f"[ComfyColab 3D] Existing pinned {name} reused "
            f"(revision: {actual})."
        )
        return target
    _run("git", "clone", "--filter=blob:none", repository, str(target))
    _run("git", "fetch", "origin", revision, "--depth", "1", cwd=target)
    _run("git", "checkout", "--detach", "FETCH_HEAD", cwd=target)
    requirements = target / "requirements.txt"
    if requirements.is_file():
        _run(
            sys.executable,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "-r",
            str(requirements),
        )
    return target


def _run_pinned_installer(repository: Path, revision: str) -> None:
    """Run a dependency's installer only when its exact audited revision is present."""
    if _commit(repository) != revision:
        print(
            f"[ComfyColab 3D] Skipping {repository.name}/install.py because "
            "the existing dependency is not the pinned revision."
        )
        return
    installer = repository / "install.py"
    if installer.is_file():
        _run(sys.executable, "install.py", cwd=repository)


def _check() -> None:
    custom_nodes = _custom_nodes_root()
    checks = {
        name: (
            (custom_nodes / name / "__init__.py").is_file()
            and _commit(custom_nodes / name) == revision
        )
        for name, _repository, revision in DEPENDENCIES
    }
    checks["standalone_entrypoint"] = (ROOT / "__init__.py").is_file()
    checks["node_list"] = (ROOT / "node_list.json").is_file()
    print(json.dumps(checks, indent=2, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit(1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        installed = {
            name: _install_dependency(name, repository, revision)
            for name, repository, revision in DEPENDENCIES
        }
        trellis = installed["ComfyUI-TRELLIS2"]
        if _commit(trellis) == DEPENDENCIES[0][2]:
            for name in TRELLIS_PATCHES:
                _apply_patch(trellis, ROOT / "patches" / name)
            _run_pinned_installer(trellis, DEPENDENCIES[0][2])
    _check()
    if not args.check:
        print(
            "[ComfyColab 3D] Base standalone installation complete. "
            "Restart ComfyUI."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
