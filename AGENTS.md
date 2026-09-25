# Project instructions

- Target **Samsung Galaxy A10 SM-A105F**, historical SLK build **A105FDDS9CWB3**. Goal: genuine native Debian 13 Trixie `arm64`, minimal headless CLI userspace; no default GUI or Android chroot.
- Read `Prompt.md`, `START_HERE.md`, `docs/STATUS.md`, and `docs/JOURNAL.md` before new work. Update status and journal at milestones and handoffs with verified branch/commit, actual build/test results, blockers and next exact task.
- Source of truth for ordinary project files is the requested **private `SM-A105F` GitHub repository** once actually created and verified. This is the latest user preference, superseding earlier public requests. Inspect remote before reconciling work; commit meaningful increments, inspect additions for secrets and private device data, then push and verify. No source license is chosen yet.
- Record exact source URLs, revision or release, retrieval date, size, SHA-256, terms, and correspondence evidence in `docs/SOURCES.md`. Keep acquired inputs immutable; store large/private inputs and outputs outside Git and record location and hashes in `docs/ARTIFACTS.md`.
- Never claim a build, test, boot, safety property, or physical capability without actual evidence. A compiled kernel or emulated userspace is not device verification.
- Never modify the phone, flash, wipe, repartition, unlock/relock, or alter boot/security, identity or calibration partitions under this instruction. Obtain explicit approval for each consequential physical operation after validating exact target and recovery route.
- Protect charging and thermal behavior. Do not assume other A10 variants match this model. Check kernel bitness and device tree against exact stock evidence before boot packaging.
- Rootfs script syntax: `bash -n scripts/build-rootfs.sh`. Build preflight and requirements are in `docs/BUILD.md`; no rootfs build has succeeded yet. Current architecture and status are in `docs/ARCHITECTURE.md` and `docs/STATUS.md`.
- Archive tool checks: `python3 -m unittest discover -s tests -v` and `python3 -m py_compile scripts/inventory-archive.py`. They do not verify a real stock archive.
