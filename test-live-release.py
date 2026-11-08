"""Synthetic end-to-end for dedicated Pinokio serve.py.

Only run from an isolated QA checkout with a cloned application source tree,
built frontend and Python dependencies. Never touches the user's live Pinokio
installation or personal library. Requires EMBER_RELEASE_QA_SANDBOX=1.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent


def call(port: int, route: str, data: dict | None = None,
         method: str = "GET") -> tuple[int, dict | str]:
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}{route}",
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Content-Type": "application/json"}, method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            if "json" in response.headers.get("Content-Type", ""):
                return response.status, json.loads(body)
            return response.status, body
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


def unused_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def start(port: int, mode: str) -> subprocess.Popen:
    env = os.environ.copy()
    env["EMBER_AUTO_INSTALL_CREATIVE_MODEL"] = "0"
    env["EMBER_AUTO_INSTALL_HIGH_HEAT_MODEL"] = "0"
    env["EMBER_AUTO_TEST_CREATIVE_MODEL"] = "0"
    stdout = (ROOT / f"qa-{mode}.stdout.log").open("w", encoding="utf-8")
    stderr = (ROOT / f"qa-{mode}.stderr.log").open("w", encoding="utf-8")
    try:
        return subprocess.Popen(
            [sys.executable, str(ROOT / "serve.py"), "--port", str(port),
             "--mode", mode], cwd=ROOT, env=env, stdout=stdout, stderr=stderr,
        )
    finally:
        stdout.close()
        stderr.close()


def await_health(process: subprocess.Popen, port: int):
    for _ in range(90):
        if process.poll() is not None:
            raise RuntimeError(f"Pinokio QA server {port} exited: {process.returncode}")
        try:
            status, payload = call(port, "/api/health")
            if status == 200 and payload.get("ok"):
                return
        except (OSError, ValueError, TimeoutError):
            pass
        time.sleep(.3)
    raise TimeoutError(f"Pinokio QA server {port} did not become healthy")


def main():
    if os.environ.get("EMBER_RELEASE_QA_SANDBOX") != "1":
        raise RuntimeError("Only explicitly isolated QA sandboxes may run this test")
    if "qa" not in str(ROOT).casefold():
        raise RuntimeError("Refusing to test within a real Pinokio author installation")
    if not (ROOT / "app/frontend/dist/index.html").is_file():
        raise RuntimeError("Candidate frontend build missing in test sandbox")
    # Hosted Pinokio serves API and UI from the SAME loopback origin.
    # Windows builds used to miss Vite's path rewrite and silently connect
    # to another user's port-8000 process. Refuse that release artifact.
    for script in (ROOT / "app/frontend/dist/assets").rglob("*.js"):
        if b"http://127.0.0.1:8000/api" in script.read_bytes():
            raise RuntimeError(
                f"Hosted bundle would contact a different API origin: {script.name}"
            )
    if not (ROOT / ".installed").is_file():
        raise RuntimeError("QA installation marker missing")

    a, b = unused_port(), unused_port()
    while b == a:
        b = unused_port()
    private = start(a, "personal")
    demo = start(b, "demo")
    try:
        await_health(private, a)
        await_health(demo, b)
        for port in (a, b):
            status, page = call(port, "/")
            assert status == 200 and "EmberWriter" in page
        status, project = call(a, "/api/projects", {
            "name": "QA Sandbox Private Project",
            "description": "Synthetic writer data only",
        }, "POST")
        assert status == 200, project
        slug = project["slug"]
        payload = {"content": "# Private QA Chapter\n\nSECRET_QA_MARKER_7129"}
        status, _ = call(a, f"/api/projects/{slug}/file?path=manuscript%2Fchapter-001.md",
                         payload, "PUT")
        assert status == 200
        status, chapter = call(a, f"/api/projects/{slug}/file?path=manuscript%2Fchapter-001.md")
        assert status == 200 and "SECRET_QA_MARKER_7129" in chapter["content"]
        status, _ = call(b, f"/api/projects/{slug}")
        assert status == 404, "Demo was able to read a private project"
        assert (ROOT / "data/projects" / slug / "manuscript/chapter-001.md").is_file()
        assert not (ROOT / "demo-data/projects" / slug).exists()
        status, _ = call(b, "/api/projects/load-path", {
            "path": str(ROOT / "data/projects" / slug),
        }, "POST")
        assert status == 403, "Demo import of private author files was not blocked"
        status, made = call(a, "/api/recovery/backup",
                            {"reason": "Pinokio isolated QA backup"}, "POST")
        assert status == 201, made
        status, verified = call(a,
            f"/api/recovery/generations/{made['id']}/verify", {}, "POST")
        assert status == 200 and verified["healthy"]
        print(json.dumps({
            "synthetic": True, "private_demo_servers_healthy": True,
            "private_demo_frontend_served": True, "private_save_read": True,
            "demo_cannot_read_private": True, "demo_path_import_blocked": True,
            "recovery_snapshot_verified": True, "actual_pinokio_gui_tested": False,
            "fresh_windows_os_tested": False, "release_qualified": False,
        }, indent=2))
    finally:
        for process in (demo, private):
            if process.poll() is None:
                process.terminate()
        for process in (demo, private):
            try:
                process.wait(timeout=12)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=8)


if __name__ == "__main__":
    main()
