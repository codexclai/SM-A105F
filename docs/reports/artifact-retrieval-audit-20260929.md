# Current missing-artifact search — 2026-09-29

## Search performed

- Queried the connected private GitHub release API for all currently listed releases and asset metadata. It lists the draft release tag `a105f-host-only-candidate-20260928` with `SM-A105F-host-only-boot-candidate-20260928.tar.gz` (12,118,381 bytes, GitHub API digest `sha256:f28d6a293695ae6075123a4ed9af0a9c5f19b0f7fe6c125c98a71e87cfd98ae5`). Metadata is not a content readback and does not verify that archive or its inner files.
- Enumerated the authorized Drive folder `SM-A105F` through the Drive connector. It returned 24 direct children and no next-page token. The list includes the exact Samsung source ZIP chunks, historical small Git bundles, and third-party Eureka build archives. It does not include an exact Samsung-built kernel Image, corrected initramfs archive, or A10 stock DTB/DTBO binaries. The source archive itself is already reassembled locally and hash-verified; do not redownload it.
- The private repository release API exposes names/sizes/digests but not binary bytes through the available GitHub content connector. Prior browser release-asset navigation ended at a Chrome download error and is not retried here. The existing Codespace was previously blocked at an interactive GitHub sign-in surface. No authentication workaround was attempted.

## Current result and next route

The exact Samsung kernel, corrected initramfs binary, and stock A10 DT/DTBO binaries remain absent from the active workspace. The existing release candidate's metadata digest must not be treated as verification of its content. A supported binary transfer/readback route is still required (for example, a user-authorized artifact attachment or normal authenticated download from the existing environment); once bytes are present, verify each against its original recorded SHA-256 and inspect internal manifests before packaging.

No replacement build was made from third-party kernel sources. No Android boot candidate was regenerated. No proprietary firmware binary was added to Git. The phone remains untouched.
