"""
User API Package.

This package contains API endpoints and controllers related to document management.
"""
from document_uploader.web.api.document.document_controller import router

__all__ = ["router"]
