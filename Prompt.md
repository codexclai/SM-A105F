# SM-A105F native Debian/Linux bring-up — project brief

## Goal

Develop and document a genuine native ARM64 Linux/Debian 13 Trixie bring-up for the Samsung Galaxy A10 SM-A105F, starting with a minimal headless userspace and expanding hardware support only when evidence supports it.

## Engineering rules

- Target the exact SM-A105F variant. Related Exynos devices are references, not proof of compatibility.
- Keep evidence levels explicit: proposed, implemented, compiled, host-tested, emulated, device-detected, device-tested, or operationally validated.
- A successful compile, DT schema check, or emulated userspace is not evidence that an image boots safely on the phone.
- Keep vendor firmware and other redistribution-restricted inputs outside Git. Record provenance, revision, size, hashes, terms, and reproducible procedures where appropriate.
- Preserve third-party authorship, licensing, SPDX identifiers, and attribution.
- Prefer reproducible scripts, configuration fragments, patches, tests, and concise engineering reports.
- Do not weaken security or invent missing hardware facts merely to make a build succeed.

## Safety boundary

Repository work may include research, code, builds, packaging, emulation, and host-side validation. Physical-device operations such as flashing, wiping, repartitioning, bootloader/recovery changes, or writes to critical partitions require a separately verified recovery plan and explicit approval for that exact operation.

## Current technical direction

Maintain exact-device Samsung 4.4.177 evidence as a compatibility reference while developing the modern Linux 6.18.x A10/Exynos bring-up track. Keep Debian userspace work separate from claims about kernel/device bootability. Root partition identity must be measured rather than guessed.

See `docs/STATUS.md` for the latest verified checkpoint, `docs/JOURNAL.md` for chronological work, `docs/SOURCES.md` for provenance, `docs/ARTIFACTS.md` for artifact records, and `docs/BUILD.md` for reproducible build procedures.

## Open-source development

Original project material is licensed under GPL-2.0-only unless a file states otherwise. Third-party material retains its own license. Contributions should follow `CONTRIBUTING.md`, and public-release/privacy checks are tracked in `PUBLIC_RELEASE_CHECKLIST.md`.
