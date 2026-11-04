# EmberWriter for Pinokio

A one-click local **author-led, full-book writing studio** for Windows x64. Bring your premise, world, characters and creative direction; EmberWriter can propose the outline and draft the whole novel while you edit, redirect and approve every chapter. The application also includes local writing-quality diagnostics, continuity reviews, PDF/EPUB/DOCX publishing tools and offline Windows audiobook narration (WAV/MP3). The first-run fictional demonstration is safely separate from your private library.

## Install with Pinokio

1. Install Pinokio 8 or later on Windows x64.
2. Choose **Download from URL** (or **Ask Pinokio → Download**, depending on your version).
3. Enter `https://github.com/grumpystrongman/EmberWriter-Pinokio` and install this launcher.
4. Click **Install**. The launcher clones the public application source from `https://github.com/grumpystrongman/EmberWriter`, creates a Python 3.11 environment, installs backend dependencies, builds the frontend and provisions/reuses Ollama.
5. After installation, click **Start DEMO (sample stories only)**, then **Open DEMO**. You can separately select **Start PRIVATE (your manuscripts)** and **Open PRIVATE**.
6. Optionally choose **Install writing model (if missing)**. Model downloads may be large. Models are not automatically pulled on launch.

Both services bind only to `127.0.0.1`. The chosen port changes between sessions. Launch from Pinokio instead of bookmarking a particular port.

## What first-run demo includes

The original, all-ages science-fantasy sample **The Lanterns of Asterfall** is created **locally during installation**. It contains sample chapters, character dossiers, a screenplay, world bible, timeline, relationships, scene cards, research notes, revision checkpoints, a sample AI Studio prompt, and nine corkboard cards. The demo uses no customer or author's private writing.

Run `python seed_showcase.py --offline` from a backend environment if the demo needs to be re-created; rerunning will not overwrite an existing demo. This mode invokes the local app in process, with no external HTTP call.

## Storage isolation and privacy

- **DEMO:** `demo-data/`, an independent project and knowledge database.
- **PRIVATE:** `data/`, a separate project and knowledge database.
- **Preferences:** `app/.ember/`, local app runtime settings. Model services (Ollama) and dependencies are shared between workspaces.
- `backups/` stores verified snapshots of both data directories when updating.

No private projects, personal databases, backups, credentials, model weights, or machine logs are included in this repository. The install pulls application source and dependencies from the public internet. The app can also support configurable model providers, so **localhost binding does not guarantee that model prompts never leave the machine**. For private use, choose a local model, verify provider URLs, and restrict outbound connectivity if needed. Do not expose the local servers to an untrusted network.

The demo disables historical project recovery, arbitrary local-folder importing, and project restore/import endpoints. This is application-level isolation, **not a security sandbox**; both processes run under the user's OS account.

## Updating and backup

**Update** stops both servers, verifies a snapshot of the personal and demo data directories, fast-forwards the application and launcher repositories, and rebuilds dependencies. **Reinstall dependencies** leaves data intact. Do not delete `data/` or `demo-data/` when updating. Keep an independent backup outside the launcher folder.

If you choose to migrate an existing local EmberWriter checkout, an optional ignored `config.local.json` may provide its path **before installation**:
```json
{"source": "C:\\path\\to\\EmberWriter"}
```
Without that file, a new installation starts with a new empty private library, separate from the installed demo.

## Developer tests

Run `node test-menu.js` to check Pinokio menu script syntax, launcher modes, and URL capture; run `python -m unittest test-deployment -v` using a compatible Python environment. Both tests use synthetic data.

Project source: https://github.com/grumpystrongman/EmberWriter

## Distribution

This repository contains only the Pinokio launcher and an original synthetic showcase generator. Pinokio can import public GitHub script repositories from their URL. Inclusion in the curated/verified Pinokio directory is a separate review process and is not guaranteed.
