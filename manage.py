"""Pinokio deployment support. No changes to the original checkout or model cache."""
from __future__ import annotations

import hashlib
from contextlib import closing
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import time
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app"


def config() -> dict:
    path = ROOT / "config.local.json"
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}


def copy_verified(source: Path, destination: Path) -> int:
    """Snapshot SQLite through its backup API, and verify every other file."""
    count = 0
    destination.mkdir(parents=True, exist_ok=False)
    for src in source.rglob("*"):
        if not src.is_file() or src.name.endswith(("-wal", "-shm", "-journal")):
            continue
        dst = destination / src.relative_to(source)
        dst.parent.mkdir(parents=True, exist_ok=True)
        with src.open("rb") as handle:
            sqlite = handle.read(16) == b"SQLite format 3\x00"
        if sqlite:
            with closing(sqlite3.connect(src.as_uri() + "?mode=ro", uri=True)) as original:
                with closing(sqlite3.connect(dst)) as snapshot:
                    original.backup(snapshot)
                    if snapshot.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                        raise RuntimeError(f"SQLite integrity check failed: {src.relative_to(source)}")
        else:
            shutil.copy2(src, dst)
            with src.open("rb") as original, dst.open("rb") as snapshot:
                if hashlib.file_digest(original, "sha256").digest() != hashlib.file_digest(snapshot, "sha256").digest():
                    raise RuntimeError(f"Copy verification failed: {src.relative_to(source)}")
        count += 1
    return count


def seed_data() -> None:
    settings = config()
    source = Path(settings.get("source", str(APP)))
    data = ROOT / "data"
    staging = ROOT / "data.migrating"
    if not data.exists():
        if staging.exists():
            raise RuntimeError("An incomplete data.migrating snapshot exists; inspect before retrying.")
        if (source / "data").is_dir() and source.resolve() != APP.resolve():
            count = copy_verified(source / "data", staging)
            staging.rename(data)
            print(f"Verified migration: {count} files; SQLite snapshots checked.", flush=True)
        else:
            (data / "projects").mkdir(parents=True)
    # App runtime preferences stay at their native path. Never delete app on reset.
    runtime = APP / ".ember"
    runtime.mkdir(exist_ok=True)
    if source.resolve() != APP.resolve() and (source / ".ember").is_dir():
        for src in (source / ".ember").glob("*.json"):
            if src.name == "image-engine-runtime.json":  # stale PID is not portable
                continue
            dst = runtime / src.name
            if not dst.exists():
                shutil.copy2(src, dst)


def ollama_executable(install: bool = False) -> str:
    candidates = [
        ROOT / "runtime" / "ollama" / "ollama.exe",
        Path(os.getenv("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe",
    ]
    found = shutil.which("ollama") or next((str(p) for p in candidates if p.is_file()), "")
    if not found and install:
        if sys.platform != "win32":
            raise RuntimeError("This launcher supports Windows x64. Install Ollama for other platforms.")
        target = ROOT / "runtime" / "ollama"
        target.mkdir(parents=True, exist_ok=True)
        archive = target / "download.zip"
        print("Downloading the official standalone Ollama Windows runtime...", flush=True)
        urllib.request.urlretrieve("https://github.com/ollama/ollama/releases/latest/download/ollama-windows-amd64.zip", archive)
        with zipfile.ZipFile(archive) as bundle:
            for entry in bundle.infolist():
                if not (target / entry.filename).resolve().is_relative_to(target.resolve()):
                    raise RuntimeError("Invalid archive path")
            bundle.extractall(target)
        archive.unlink()
        found = str(target / "ollama.exe")
    if found:
        os.environ["PATH"] = str(Path(found).parent) + os.pathsep + os.environ.get("PATH", "")
    return found


def backup() -> Path:
    target = ROOT / "backups" / time.strftime("%Y%m%d-%H%M%S")
    target.mkdir(parents=True, exist_ok=False)
    count = copy_verified(ROOT / "data", target / "data")
    if (ROOT / "demo-data").is_dir():
        count += copy_verified(ROOT / "demo-data", target / "demo-data")
    runtime = APP / ".ember"
    if runtime.exists():
        (target / ".ember").mkdir()
        for src in runtime.glob("*.json"):
            shutil.copy2(src, target / ".ember" / src.name)
    print(f"Backup verified: {count} data files at {target}", flush=True)
    return target


def models() -> None:
    executable = ollama_executable(install=True)
    sys.path.insert(0, str(APP / "backend"))
    import asyncio
    from app.ollama_runtime import ensure_ollama_ready
    from app.model_preferences import preferred_local_model
    from app.model_catalog import GENERAL_PROSE_MODEL
    asyncio.run(ensure_ollama_ready("http://127.0.0.1:11434"))
    model = config().get("model") or preferred_local_model() or GENERAL_PROSE_MODEL
    subprocess.run([executable, "pull", model], check=True)


def main() -> None:
    mode = sys.argv[1]
    if mode == "install":
        seed_data()
        executable = ollama_executable(install=True)
        subprocess.run([executable, "--version"], check=True)
        (ROOT / ".installed").write_text("Installation completed\n", encoding="utf-8")
        print("EmberWriter installed. Existing Ollama models reused; use Install writing model if needed.", flush=True)
    elif mode == "backup":
        backup()
    elif mode == "models":
        models()
    else:
        raise ValueError(mode)


if __name__ == "__main__":
    main()
