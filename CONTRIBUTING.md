# Contributing

Thanks for your interest in the SM-A105F native Linux/Debian bring-up project.

## Project principles

This project values reproducibility and accurate evidence. Please distinguish between work that is proposed, implemented, compiled, host-tested, emulated, device-tested, and verified on physical hardware.

Do not describe a build as bootable or safe to flash unless that exact result has been tested and documented.

## Contributions

Useful contributions include:

- SM-A105F and Exynos 7884B/7885 device-tree research;
- kernel patches and configuration improvements;
- build and test tooling;
- Debian ARM64 userspace work;
- documentation and source-provenance corrections;
- reproducible test cases and validation.

Keep changes focused and explain what was changed, why, and how it was tested.

## Licensing and third-party material

Do not commit Samsung firmware, proprietary binaries, private vendor material, or other third-party content unless its redistribution terms clearly allow it.

Preserve upstream authorship, copyright notices, SPDX identifiers, and license information when adapting existing open-source work.

When adding a source or external artifact reference, document its origin and exact revision where practical.

## Privacy and secrets

Never commit passwords, API keys, access tokens, cookies, private keys, personal device identifiers, private account links, or other credentials.

## Hardware safety

Do not present unverified flashing instructions as safe. Any future physical-device testing should identify the exact target variant, recovery path, expected risk, and evidence supporting the operation.

## Tests

Run the checks relevant to your change and record the actual result. Common host-side checks include:

```sh
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/inventory-archive.py
bash -n scripts/build-rootfs.sh
```

Kernel and device-tree changes should include the exact source revision, configuration, command, and validation result where possible.

## Issues and pull requests

When reporting a problem, include the exact SM-A105F context, relevant logs, source revision, and steps to reproduce. Please avoid uploading proprietary firmware or private device information in issues.
