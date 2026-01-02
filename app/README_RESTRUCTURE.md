# Restructure Notes

This file documents the recent reorganization to match the requested structure.

Key changes:
- Added `app/api/deps.py` and `app/api/v1/` wrapper modules for API versioning
- Created `app/domain/exceptions` and moved exceptions into `base.py` and added a compatibility shim at `app/exceptions/exceptions.py`
- Added `app/core` shims for `config`, `security`, and `hashing` (backwards-compatible)
- Added placeholder domain rules in `app/domain/rules`

Next steps:
- Move and refactor service/repository modules into smaller domain-specific modules as needed
- Update imports across the codebase to point to the new modules (done partially)
- Run full test-suite and fix any remaining import or runtime errors

If you want, I can now proceed to fully move more modules (services, repositories) into the exact folders you listed and update all imports automatically.