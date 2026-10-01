# Native Debian for Samsung Galaxy A10 SM-A105F

Engineering project for a minimal, headless, native Debian 13 `arm64` system on the **SM-A105F**. The historical reference firmware is `A105FDDS9CWB3` for `SLK`. This repository is at the investigation stage: it contains no bootable image and no physically verified port.

Read [START_HERE.md](START_HERE.md) to resume work, [Prompt.md](Prompt.md) for governing requirements, [docs/STATUS.md](docs/STATUS.md) for the authoritative current state, and [docs/JOURNAL.md](docs/JOURNAL.md) for engineering history. [docs/SOURCES.md](docs/SOURCES.md) distinguishes located sources from acquired and verified inputs.

The first architecture gate is whether an exact-device kernel and boot chain can run an AArch64 kernel and userspace. A 64-bit SoC alone does not establish that. A related A10 kernel project builds with `ARCH=arm64`, but this does not establish compatibility with the exact stock firmware. No operation in this repository authorizes flashing or changing a physical device.

Original project material is released under the GNU General Public License v2.0 only (GPL-2.0-only), as described in [LICENSE](LICENSE). Third-party materials retain their own licenses; do not redistribute firmware or vendor source without reviewing its terms.

This repository is being prepared for public open-source development. See [CONTRIBUTING.md](CONTRIBUTING.md) and [PUBLIC_RELEASE_CHECKLIST.md](PUBLIC_RELEASE_CHECKLIST.md). No claim of production readiness or physical-device validation is made.
