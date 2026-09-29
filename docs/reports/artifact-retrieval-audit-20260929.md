# Current missing-artifact search — 2026-09-29

## Search performed

- Queried the connected private GitHub release API for all currently listed releases and asset metadata. It lists the draft release tag `a105f-host-only-candidate-20260928` with `SM-A105F-host-only-boot-candidate-20260928.tar.gz` (12,118,381 bytes, GitHub API digest `sha256:f28d6a293695ae6075123a4ed9af0a9c5f19b0f7fe6c125c98a71e87cfd98ae5`). Metadata is not a content readback and does not verify that archive or its inner files.
- Enumerated the authorized Drive folder `SM-A105F` through the Drive connector. It returned 24 direct children and no next-page token. The list includes the exact Samsung source ZIP chunks, historical small Git bundles, and third-party Eureka build archives. It does not include an exact Samsung-built kernel Image, corrected initramfs archive, or A10 stock DTB/DTBO binaries. The source archive itself is already reassembled locally and hash-verified; do not redownload it.
- The private repository release API exposes names/sizes/digests but not binary bytes through the available GitHub content connector. Prior browser release-asset navigation ended at a Chrome download error and is not retried here. The existing Codespace was previously blocked at an interactive GitHub sign-in surface. No authentication workaround was attempted.

## Current result and next route

The exact Samsung kernel, corrected initramfs binary, and stock A10 DT/DTBO binaries remain absent from the active workspace. The existing release candidate's metadata digest must not be treated as verification of its content. A supported binary transfer/readback route is still required (for example, a user-authorized artifact attachment or normal authenticated download from the existing environment); once bytes are present, verify each against its original recorded SHA-256 and inspect internal manifests before packaging.

No replacement build was made from third-party kernel sources. No Android boot candidate was regenerated. No proprietary firmware binary was added to Git. The phone remains untouched.


## 2026-09-29 connector transfer recheck

The project Drive folder was listed again. It still contains the three original Samsung source ZIP chunks (80 MiB, 80 MiB, and 62,045,634 bytes), the checkpoint, older Eureka bundles/configs, and small Git bundles; no exact Samsung-built 4.4.177 kernel output, corrected initramfs archive, or stock A10 DT/DTBO image appeared. Targeted Drive searches for the kernel, corrected initramfs, and DT/DTBO also returned only the checkpoint.

The Drive helper's file-transfer operation rejected source part-02 at the executor's 32 MiB per-file limit. Its supported signed raw-file URL was then streamed with `curl` to the workspace; all three chunks (80 MiB, 80 MiB, and 62,045,634 bytes) were obtained. Concatenation produced the original 229,817,794-byte ZIP with SHA-256 `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`, exactly matching the recorded archive hash. `unzip -t` passed. The embedded `Kernel.tar.gz` was extracted and independently matched its recorded 202,050,103-byte SHA-256 `e05288db460f2d0a0f86c79beac819066f4ea3baa57cf5f26b46cdf4ec3d0af2`. This is verified source recovery, not recovery of a Samsung-built kernel output.

No release candidate bytes or unverified binaries were treated as recovered. No boot-v1 artifact was regenerated. Phone remains untouched.


The rehydrated Samsung source archive and embedded kernel source archive remain in transient workspace storage only. They are not committed to Git; the archive hashes above are the durable integrity record. The exact A10 oscillator source evidence was used to update the Linux 6.18 A10 board patch; see the validation report. Exact built `Image`, corrected initramfs and stock A10 DT/DTBO binaries remain unavailable.
