# Project instructions

## Session and engineering rules

- Start each fresh session by reading `Prompt.md`, `START_HERE.md`, this file, `docs/STATUS.md`, `docs/JOURNAL.md`, `docs/SOURCES.md`, and `docs/ARTIFACTS.md`; reconcile remote, local, and artifact state before acting. Chat memory is not shared between sessions; durable project files are the continuity source.
- Make routine, reversible project edits and host-side checks autonomously inside the repository. Keep physical-device changes, purchases, repository visibility changes, and unrelated account operations outside this project's authority. Do not run destructive commands, use full-access bypasses, or force-push.
- Preserve end-to-end responsibility: inspect diffs, run relevant checks, update evidence and checkpoint, and synchronize only through a verified authorized GitHub/Drive workflow. A local commit is not proof of remote synchronization.

- Target **Samsung Galaxy A10 SM-A105F**, historical SLK build **A105FDDS9CWB3**. Goal: genuine native Debian 13 Trixie `arm64`, minimal headless CLI userspace; no default GUI or Android chroot.
- Read `Prompt.md`, `START_HERE.md`, `docs/STATUS.md`, and `docs/JOURNAL.md` before new work. Update status and journal at milestones and handoffs with verified branch/commit, actual build/test results, blockers and next exact task.
- Source of truth for ordinary project files is the verified **SM-A105F GitHub repository** on `main`. The pre-GitHub local commit chain is preserved in verified external recovery bundles and has different ancestry from the remote source snapshot. Inspect remote before reconciling work; commit meaningful increments, inspect additions for secrets and private device data, then publish and verify without rewriting unrelated history. Original project material is licensed GPL-2.0-only; preserve third-party licensing and attribution separately.
- Record exact source URLs, revision or release, retrieval date, size, SHA-256, terms, and correspondence evidence in `docs/SOURCES.md`. Keep acquired inputs immutable; store large/private inputs and outputs outside Git and record location and hashes in `docs/ARTIFACTS.md`.
- Never claim a build, test, boot, safety property, or physical capability without actual evidence. A compiled kernel or emulated userspace is not device verification.
- Never modify the phone, flash, wipe, repartition, unlock/relock, or alter boot/security, identity or calibration partitions under this instruction. Obtain explicit approval for each consequential physical operation after validating exact target and recovery route.
- Protect charging and thermal behavior. Do not assume other A10 variants match this model. Check kernel bitness and device tree against exact stock evidence before boot packaging.
- Rootfs script syntax: `bash -n scripts/build-rootfs.sh`. Build preflight and requirements are in `docs/BUILD.md`; no rootfs build has succeeded yet. Current architecture and status are in `docs/ARCHITECTURE.md` and `docs/STATUS.md`.
- Archive tool checks: `python3 -m unittest discover -s tests -v` and `python3 -m py_compile scripts/inventory-archive.py`. They do not verify a real stock archive.
- Also read [`docs/WORK_SESSION_CONTINUATION.md`](docs/WORK_SESSION_CONTINUATION.md): the owner is the primary human authority, may work with this session directly, and does not need another ChatGPT conversation's approval. A relayed prompt applies when the owner presents/adopts it. Continue safe independent work autonomously without implying persistent work after the session ends.
