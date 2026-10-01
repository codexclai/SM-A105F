# Security

This repository contains experimental low-level Linux/device bring-up work for the Samsung Galaxy A10 SM-A105F.

If you find a security-sensitive issue, please avoid publishing credentials, private device identifiers, exploit details affecting an unpatched third party, or other sensitive information in a public issue.

For ordinary project bugs, build failures, documentation problems, and non-sensitive hardware-support issues, use the repository issue tracker once it is public.

## Secrets

No password, API key, access token, cookie, SSH private key, signing key, or other credential should ever be committed to this repository. If one is accidentally committed, revoke or rotate it first; deleting the visible file alone is not sufficient because Git history may retain it.

## Firmware and device data

Do not upload proprietary firmware merely to reproduce a bug. Do not publish IMEI/serial numbers, account identifiers, or unique private device data.

## Experimental artifacts

Compiled kernels, DTBs, initramfs files, or boot images are not automatically safe to flash. Security and recovery implications must be evaluated separately from whether an artifact successfully compiles.
