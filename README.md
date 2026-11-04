# EmberWriter for Pinokio

A one-click local **author-led, full-book writing studio** for Windows x64. Bring your premise, world, characters and creative direction; EmberWriter can propose the outline and draft the whole novel while you edit, redirect and approve every chapter. The application also includes local writing-quality diagnostics, continuity reviews, PDF/EPUB/DOCX publishing tools and offline Windows audiobook narration (WAV/MP3). The first-run fictional demonstration is safely separate from your private library.

## Simplified, tested interface

The desktop starts with Write, Studio, Plan, Analyze and Publish, with less-frequently-used tools behind **More**. Plan is organized into four task groups instead of eleven competing tabs; publishing has six focused stages. At narrow window sizes, Write, Plan and Publish stay directly accessible. A synthetic-only visual smoke test verifies the layout at 1440, 900 and 390 pixels without opening or uploading private manuscripts.

## What's included

- **Book Production Conductor:** one durable author-led flow from chapter planning through queued draft generation, opt-in independent reader critiques, mandatory author decisions, whole-book editorial checks and publishing handoff. Includes local checkpoint history and a Prompt Context Inspector.
- **Book Studio:** author-approved whole-book drafting, background generation, pause/resume, chapter editing and local reader critique.
- **Whole-Book Editorial Board:** consolidated Prose Editor and Style Bible scan, reader/arc coverage, chapter priorities, author-approved batch corrections, and exportable editorial review.
- **Prose Editor + Style Bible:** offline mechanical grammar suggestions, terminology consistency, reviewable exceptions, and rollback snapshots.
- **Revision Workbench:** evidence-backed suggestions and author-approved side-by-side alternatives.
- **Story Arc Investigator + Dossier:** opt-in local AI analysis of narrative decisions, consequences, relationships and possible foreshadowing, all tied to exact source quotes.
- **Manuscript Intelligence + Voiceprint Lab:** cross-chapter observations and comparison against your preferred authored prose rhythm.
- **Production Readiness Gate:** a written author sign-off on draft, continuity, proofreading, Binder and metadata warnings.
- **Audiobook direction:** private spoken-name substitutions, per-chapter narrator and pacing profiles, timestamped proof-listening notes, and an author-controlled QC gate. Heavy writing, review and narration steps coordinate through a single-server-process resource slot; multi-worker and external model sessions are not globally locked.
- **Audiobook Workshop:** offline Windows SAPI narration for one chapter or a persistent Binder-ordered whole-book queue, configurable speech pacing, pause/resume and restart recovery. WAV/MP3 chapter packages, version-aware technical audio readiness checks, and optional locally encoded **chapter-marked M4B** exports via FFmpeg/FFprobe. The audio remains private and is not a professional mastered recording.

This is a local-first writing and book-production studio. AI and heuristic observations are advisory; professional grammar certification, studio-quality multi-voice audiobook mastering, and retailer acceptance are not implied. New features are released through the public application repository and installed using **Update** in Pinokio.

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
