# A10 RAM and fixed reservations — Linux 6.18.54 review

## Decision

Add the exact two populated A10 RAM banks, retain the Samsung top-level memreserve entry, and represent the nine fixed occupied regions as generic /reserved-memory children with reg only. This prevents the Linux memory allocator from handing those physical ranges to ordinary allocations.

The node names and ranges preserve source identity; they do not claim that Linux has implemented Android ION, modem, GNSS, framebuffer, secure-monitor, or logging consumers. Dynamic pools, vendor compatibles, allocator properties, secure/no-map behavior, and reusable semantics remain unresolved and are not copied.

## Exact Samsung source evidence

- Base Samsung source exynos7885.dts, SHA-256 9d6b88c24a05ba20cf49de666f9775a9437df6911459902017e92f8bb8264f79, declares populated RAM banks:
  - 0x80000000 through 0xBDA00000, size 0x3DA00000.
  - 0xC0000000 through 0x100000000, size 0x40000000.
- Samsung exynos7885-rmem.dtsi, SHA-256 22582d0fff84c495c8b3032b51fc851867bfdab1d380d68f2308920c7fd7a8dc, declares /memreserve/ 0xE0000000 0x00D00000 and fixed reserved ranges listed below.
- A10-specific exynos7884-rmem_7884.dtsi, SHA-256 043800953207d58aa7005841fe7b774cb58e678dfc763e35396a4a8b3b09afc6, repeats the ABOX range at 0xE9400000 size 0x00400000. The common A10 overlay is exynos7884B-a10_common.dtsi, SHA-256 b3f7ae8a2cfb47fcc0171f8797fa2110c15182643cb26e814208e2c2be625083.
- Exact A10 SWA board overlay exynos7884B-a10_swa_open_00.dts has SHA-256 fc8c46364754e059189ba2014725ebf0321e8b315da2ddb0ba87970f60f92881. It identifies the SWA OPEN 00 source family. This is not proof of the stock device's selected DTBO.

## Fixed physical ranges

| Region | Start | Size | End exclusive | RAM bank |
| --- | ---: | ---: | ---: | --- |
| Top-level memreserve | 0xE0000000 | 0x00D00000 | 0xE0D00000 | 0x80000000 bank |
| sec-debug | 0x80000000 | 0x00001000 | 0x80001000 | 0x80000000 bank |
| TIMA | 0xB8000000 | 0x00200000 | 0xB8200000 | 0x80000000 bank |
| seclog | 0xC0000000 | 0x00080000 | 0xC0080000 | 0xC0000000 bank |
| Wi-Fi/BT | 0xE9000000 | 0x00400000 | 0xE9400000 | 0xC0000000 bank |
| ABOX | 0xE9400000 | 0x00400000 | 0xE9800000 | 0xC0000000 bank |
| Framebuffer handover | 0xEC000000 | 0x01400000 | 0xED400000 | 0xC0000000 bank |
| Modem interface | 0xF5400000 | 0x08800000 | 0xFDC00000 | 0xC0000000 bank |
| CP RAM logging | 0xFDC00000 | 0x02000000 | 0xFFC00000 | 0xC0000000 bank |
| GNSS | 0xFFC00000 | 0x00400000 | 0x100000000 | 0xC0000000 bank |

The fixed intervals are contained in the two populated DRAM banks and do not overlap each other. The 13 MiB memreserve interval is separate from the nine fixed children and also lies inside the second bank.

## Linux 6.18 mapping and limits

The upstream reserved-memory binding accepts a parent with #address-cells, #size-cells and ranges, and fixed children with reg. Linux 6.18's generic reserved-memory handling consumes these ranges for allocation exclusion. No consumer references are added.

The Samsung source also defines dynamic Bluetooth/ABOX, crypto, video-stream, and A10 video-frame allocations. Their sizing, allocation ranges, reuse/security properties, and ION consumers require old allocator and secure-monitor semantic mapping. They are omitted. A zero-sized extra memory node in the Samsung SoC file is likewise not carried into the Linux board DTS.

The fixed source nodes contain vendor-specific properties in addition to addresses. This patch copies only physical occupancy. In particular, it does not infer no-map from names such as TIMA or sec-debug, nor infer that these regions are safe to expose through Linux's linear map. The exact downstream mappings/consumers must be traced before selecting no-map, reusable, or any consumer assignment. This remains an unresolved boot-safety review item.

## Patch and validation

Patch: patches/linux-6.18.54/0004-arm64-dts-exynos-reserve-a10-fixed-memory.patch.

On Linux 6.18.54 source commit 1b357ecb321392158d507b04672ffee57bfa071d:

- The generated unified patch passed `git apply --check` in an isolated worktree reconstructed from the pre-reservation A10 DTS; applying it produced a byte-identical DTS to the already-built source.
- git diff --check exited 0.
- make -s ARCH=arm64 dt_binding_check DT_SCHEMA_FILES=reserved-memory/reserved-memory.yaml exited 0. Kernel tooling noted optional yamllint was not installed.
- make -s -j2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- CHECK_DTBS=y exynos/exynos7885-a10.dtb exited 0.
- Direct dt-validate exited 0 and emitted the existing unrelated board-root compatible mismatch (the Samsung string contains spaces and is not accepted by generic/board schemas) and osc-clock missing clock-frequency diagnostic. No reserved-memory node diagnostic was emitted. These genuine existing problems were not suppressed or changed in this milestone.
- fdtdump confirmed /memreserve/ 0xe0000000 0xd00000; fdtget read back all nine child reg tuples listed above.
- Resulting A10 DTB SHA-256: ea5b3131cfa55e02472d6f74815082282f0e3b8940471311545e558d380905b7.

This is compile/schema/DTB-content evidence only. It does not prove the bootloader supplies the same RAM map, A10 firmware selected this overlay, Linux 6.18 safely owns these regions, or the board boots. No physical-device operation occurred.
