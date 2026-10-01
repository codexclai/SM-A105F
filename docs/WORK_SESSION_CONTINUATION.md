# Engineering continuation guide

This file describes how to resume technical work without relying on private chat or account history.

## Resume procedure

1. Read `Prompt.md`, `START_HERE.md`, `AGENTS.md`, `docs/STATUS.md`, `docs/JOURNAL.md`, `docs/SOURCES.md`, `docs/ARTIFACTS.md`, `docs/ARCHITECTURE.md`, and `docs/BUILD.md`.
2. Inspect the current branch, commit, tree, working state, and recent changes before editing.
3. Reconcile every artifact needed for the next task against its recorded filename, size, SHA-256, provenance, and status.
4. Re-run relevant host checks. Do not promote evidence beyond what was actually tested.
5. Continue the next safe engineering task recorded in `docs/STATUS.md`.
6. Keep large or redistribution-restricted inputs outside Git.
7. Update documentation and tests with each coherent engineering milestone.

## Project target

The exact target is Samsung Galaxy A10 SM-A105F. The goal is native Debian 13 Trixie ARM64 with a minimal headless userspace and progressively verified hardware support.

Related Exynos7884B/7885 devices and third-party kernels may provide research context but are not exact-target validation.

## Evidence discipline

Classify results as proposed, implemented, compiled, host-tested, emulated, device-detected, device-tested, or operationally validated. Compilation and schema validation do not establish physical-device behavior.

## Artifact and source discipline

Record source URLs, revisions, retrieval dates, hashes, licensing/redistribution information, build procedures, and test results. Keep proprietary firmware, private device data, credentials, and large generated artifacts outside the repository.

## Physical-device boundary

Research, code, builds, packaging, and host-side validation may proceed without changing the phone. Flashing, wiping, repartitioning, bootloader/recovery changes, or critical-partition writes require an exact compatibility review, recovery path, and explicit approval for that operation.

## Handoff

At a stopping point, update the durable project files with the verified state, blockers, failed approaches, and the next exact engineering action. Do not depend on chat memory for project continuity.
