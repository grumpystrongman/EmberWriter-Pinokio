# EmberWriter for Pinokio — 0.16.0 RC1

**Public test release / prerelease, not a stable certified release.** Windows x64 and Pinokio 8+.

## What this launcher installs
The **RC1 launcher branch** is a separate public GitHub prerelease and pins fresh installs to the immutable application tag `preview-0.16.0-rc.1` from [EmberWriter](https://github.com/grumpystrongman/EmberWriter). The default `main` launcher remains on its independently published application track. The application release target is **0.16.0 RC1**, with a versioned GitHub prerelease and 0.16.0-rc.1 package metadata. Its install flow creates a local Python 3.11 environment, builds the frontend, preserves separate Demo and Private libraries, and offers optional writing models. Source code and synthetic QA fixtures are not your manuscript data.

## New in this release
- Series evidence/continuity navigation, semantic context proposals, reviewable scene planning, author-controlled revision handoff, a clearer writing UI, and better responsive accessibility.
- Verified isolated synthetic browser story handoff, no automatic manuscript overwrites, and disk-full interruption tests.
- Local automated accessibility scans: no violations across 18 synthetic screen/viewport combinations.

## Safe installation
1. Get Pinokio 8+ on Windows x64. Choose **Download from URL**, enter `https://github.com/grumpystrongman/EmberWriter-Pinokio`, and **select branch `release/0.16.0-rc.1`**. Do not select the default branch if you want this versioned preview.
2. New installs: click **Install**, then **Start DEMO** and **Open DEMO**. Personal writing uses a separate **Start PRIVATE** action.
3. Existing installs: make a separate verified backup of Private writing and preferences. The RC1 installer does **not** silently migrate a previous main-branch installation; use a separate RC1 Pinokio install or upgrade intentionally after backup. Update keeps branch checkouts on fast-forward pulls and pinned RC installations on their tagged revision; it rejects local source edits.
4. Optional installed model downloads are explicit and may be large. Offline operation requires dependencies and models to have been installed in advance.

## Limitations
- This is a **release candidate**, not a 38-of-38 independently certified 5/5 stable release.
- Fresh-device Pinokio GUI install/upgrade/rollback/uninstall, NVDA/manual zoom, and full publication-device and real-model quality tests remain technical deltas.
- The launcher must not be taken as a guarantee of professional audiobook mastering, distributor acceptance, or zero data loss.

See the [application RC1 release notes](https://github.com/grumpystrongman/EmberWriter/blob/main/RELEASE_NOTES_0.16.0_RC1.md) and the [application prerelease](https://github.com/grumpystrongman/EmberWriter/releases).

## Versioned preview verification
A fresh disposable Pinokio installer-directory test cloned the application, checked out the exact immutable release commit `c7498b6127afa35c360a3941d5ecd363c5fadc96`, and repeated the pinned update without changing that commit. Menu isolation tests and 2 Python deployment tests passed. This is a **launcher contract test**, not a hands-on Pinokio GUI certification.

**Security qualification:** The full application integration PR still has open SonarCloud findings when compared against default `main`. Install RC1 into a separate DEMO/test library only; do not treat this tagged preview as a hardened production build or accept unknown/untrusted manuscript uploads until the remaining findings are triaged.
