# Public release readiness checklist

This repository is being prepared for an eventual public open-source release. Do not change repository visibility until this checklist has been reviewed.

## Required before public release

- [x] Select and add an OSI-approved license for original project material — GPL-2.0-only.
- [ ] Audit every tracked file and Git history for credentials, tokens, private URLs, personal information, and account-specific identifiers.
- [x] Remove or generalize private Google Drive folder links and private draft-release URLs from the current public-facing documentation.
- [x] Replace Prompt.md and the main continuation/start documents with public engineering guidance.
- [ ] Confirm that no Samsung firmware, proprietary vendor archive, or other redistributability-restricted binary is tracked.
- [ ] Keep large firmware/source archives and build outputs outside Git unless redistribution terms clearly permit publication.
- [ ] Review third-party patches and copied material individually and preserve their original licensing and attribution.
- [ ] Rewrite README.md for public contributors with project scope, current status, build/test boundaries, roadmap, and contribution instructions.
- [x] Add CONTRIBUTING.md and a security/reporting policy.
- [ ] Re-run tests and documentation checks from a clean checkout.
- [ ] Verify the public-facing repository contains no claim that the port boots or works on hardware unless that has actually been tested.
- [ ] Audit and, if necessary, rewrite historical Git objects before changing repository visibility. Current-tree cleanup does not remove sensitive references from older commits.
- [ ] Only then change repository visibility to public.

## Current safety boundary

The physical SM-A105F has not been modified by this project. A successful compile, DT schema check, host test, or emulation result is not proof that a produced image is safe to flash or that the phone boots it.

Third-party firmware, vendor source, and other external materials retain their own licenses and redistribution terms.
