# Start here

This is the entry point for the Samsung Galaxy A10 **SM-A105F** native Linux/Debian bring-up project.

## Resume engineering work

1. Read `Prompt.md`, `AGENTS.md`, `docs/STATUS.md`, `docs/JOURNAL.md`, `docs/SOURCES.md`, `docs/ARTIFACTS.md`, `docs/ARCHITECTURE.md`, and `docs/BUILD.md`.
2. Inspect the current branch, commit, tree, and recent changes before editing.
3. Follow the next verified engineering action in `docs/STATUS.md`; do not repeat completed checks without a reason.
4. Verify required external artifacts by filename, size, SHA-256, provenance, and redistribution status.
5. Keep evidence levels precise. A build or emulation result is not physical-device validation.
6. Keep large, proprietary, private, or redistribution-restricted inputs outside Git.
7. Run relevant tests, inspect changes for secrets/private data, update the engineering journal/status, and make coherent commits.

## Target

- Device: Samsung Galaxy A10 SM-A105F
- Architecture: ARM64/AArch64
- Userspace goal: Debian 13 Trixie
- Initial interface: minimal/headless
- Modern kernel track: Linux 6.18.x A10/Exynos bring-up
- Compatibility/reference track: exact-device Samsung 4.4.177 evidence

## Safety

The physical phone is not modified merely by working on this repository. Do not flash, wipe, repartition, alter bootloader/recovery, or write critical partitions without an exact compatibility review, a credible recovery route, and explicit approval for that operation.

## Contributing

Read `CONTRIBUTING.md` before submitting changes. Original project material is GPL-2.0-only unless stated otherwise; third-party material retains its original licensing.
