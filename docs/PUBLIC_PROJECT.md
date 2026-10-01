# Public project overview

## Mission

Bring up a modern native Linux kernel and Debian 13 ARM64 userspace on the Samsung Galaxy A10 SM-A105F using reproducible, evidence-driven engineering.

The project is experimental. It does not currently claim a physically verified bootable release.

## Why this work is useful

The SM-A105F is an older Exynos-based handset with limited modern upstream support. The repository collects exact-device research, device-tree work, kernel patches, build configuration, validation tooling, provenance records, and reproducible engineering reports so that the work can be inspected and improved publicly.

## Active development areas

- Linux 6.18.x Exynos7885/SM-A105F device-tree support
- RTC, watchdog, reset and poweroff platform support
- eMMC/root-storage configuration
- Debian 13 ARM64 userspace and initramfs tooling
- schema, compilation and regression validation
- exact-device source/provenance research

## Compute requirements

Kernel development benefits from persistent Linux build infrastructure. Kernel trees, toolchains, firmware/source references, dependencies and build outputs can consume tens of gigabytes. Compilation and validation can also run long enough that a persistent remote environment is substantially more practical than an interactive browser session.

A useful development environment is therefore approximately:

- 4 vCPU
- 4–5 GiB RAM
- 30 GiB or more persistent storage, with additional storage useful
- SSH access and ordinary Linux development tools

These are development needs rather than a claim that every contribution requires that capacity.

## Project integrity

The repository distinguishes implementation and host validation from physical-device testing. It does not manufacture activity, compatibility claims, users, stars, or test results. Contributions and infrastructure support should be evaluated from the actual public history and technical work.

## Licensing

Original project material is GPL-2.0-only unless a file states otherwise. Third-party material retains its own licensing and attribution. Proprietary or redistribution-restricted firmware is not intended to be published in this repository.
