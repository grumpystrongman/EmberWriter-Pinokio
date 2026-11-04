"""Serve the production UI and existing API from one loopback origin."""
import argparse
import os
import sys

from manage import APP, ROOT, ollama_executable


def create_app(mode: str = "personal"):
    if not (ROOT / ".installed").exists():
        raise RuntimeError("Installation is incomplete. Run Install before starting EmberWriter.")
    if mode not in ("personal", "demo"):
        raise ValueError("Unknown workspace mode")
    # Data root must be set before importing the API's storage module.
    data_dir = ROOT / ("demo-data" if mode == "demo" else "data")
    data_dir.mkdir(parents=True, exist_ok=True)
    os.environ["EMBER_DATA_DIR"] = str(data_dir)
    os.environ["EMBER_WORKSPACE_MODE"] = mode
    # Explicit model installation is available from the launcher; avoid surprise downloads.
    os.environ["EMBER_AUTO_INSTALL_CREATIVE_MODEL"] = "0"
    os.environ["EMBER_AUTO_TEST_CREATIVE_MODEL"] = "0"
    os.environ["EMBER_AUTO_INSTALL_HIGH_HEAT_MODEL"] = "0"
    ollama_executable()
    sys.path.insert(0, str(APP / "backend"))
    from app.main import app
    from fastapi.responses import JSONResponse
    if mode == "demo":
        # Demo must never scan/import the user's historical or arbitrary local paths.
        @app.middleware("http")
        async def deny_demo_disk_imports(request, call_next):
            if request.url.path in (
                "/api/projects/load-path", "/api/projects/recover",
                "/api/projects/restore-upload", "/api/projects/import",
            ):
                return JSONResponse({"detail": "Disk import and recovery are unavailable in demo mode"}, status_code=403)
            response = await call_next(request)
            response.headers["X-Ember-Workspace"] = "demo"
            return response
    from fastapi.staticfiles import StaticFiles
    dist = APP / "frontend" / "dist"
    if not (dist / "index.html").is_file():
        raise RuntimeError("UI build is missing. Run Install in Pinokio.")
    app.mount("/", StaticFiles(directory=dist, html=True), name="studio")
    return app


if __name__ == "__main__":
    import uvicorn
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--mode", choices=("personal", "demo"), default="personal")
    args = parser.parse_args()
    uvicorn.run(create_app(mode=args.mode), host="127.0.0.1", port=args.port)
