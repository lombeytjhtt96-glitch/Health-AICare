"""Deprecated — CodeCleanupService has moved to app.utils.code_cleanup.

This shim exists only for backward compatibility.  Update any imports to:

    from app.utils.code_cleanup import CodeCleanupService
"""
# Re-export so existing code that still imports from the old path continues to work.
from app.utils.code_cleanup import CodeCleanupService  # noqa: F401

__all__ = ["CodeCleanupService"]
