# EmberWriter for Pinokio — 0.16.0 RC1

**Public test release / prerelease, not a stable certified release.** Windows x64 and Pinokio 8+.

## What this launcher installs
The launcher is a separate public GitHub repository and installs the current public `main` of [EmberWriter](https://github.com/grumpystrongman/EmberWriter). The application release target is **0.16.0 RC1**, with a versioned GitHub prerelease and 0.16.0-rc.1 package metadata. Its install flow creates a local Python 3.11 environment, builds the frontend, preserves separate Demo and Private libraries, and offers optional writing models. Source code and synthetic QA fixtures are not your manuscript data.

## New in this release
- Series evidence/continuity navigation, semantic context proposals, reviewable scene planning, author-controlled revision handoff, a clearer writing UI, and better responsive accessibility.
- Verified isolated synthetic browser story handoff, no automatic manuscript overwrites, and disk-full interruption tests.
- Local automated accessibility scans: no violations across 18 synthetic screen/viewport combinations.

## Safe installation
1. Get Pinokio 8+ on Windows x64. Choose **Download from URL** and enter `https://github.com/grumpystrongman/EmberWriter-Pinokio`.
2. New installs: click **Install**, then **Start DEMO** and **Open DEMO**. Personal writing uses a separate **Start PRIVATE** action.
3. Existing installs: make a separate verified backup of Private writing and preferences before clicking **Update**. Stop any active writer/generator task. Update uses fast-forward Git pulls; it **will not discard local edits or forcibly overwrite diverged checkouts**.
4. Optional installed model downloads are explicit and may be large. Offline operation requires dependencies and models to have been installed in advance.

## Limitations
- This is a **release candidate**, not a 38-of-38 independently certified 5/5 stable release.
- Fresh-device Pinokio GUI install/upgrade/rollback/uninstall, NVDA/manual zoom, and full publication-device and real-model quality tests remain technical deltas.
- The launcher must not be taken as a guarantee of professional audiobook mastering, distributor acceptance, or zero data loss.

See the [application RC1 release notes](https://github.com/grumpystrongman/EmberWriter/blob/main/RELEASE_NOTES_0.16.0_RC1.md) and the [application prerelease](https://github.com/grumpystrongman/EmberWriter/releases).
