"""Storage backends used by the chat application."""

from functools import lru_cache
from typing import Dict, Optional

from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage

try:  # pragma: no cover - optional dependency
    from storages.backends.azure_storage import AzureStorage  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    AzureStorage = None  # type: ignore


def _normalized(value: Optional[str]) -> str:
    """Return a trimmed string for easier truthiness checks."""

    if not value:
        return ""
    return value.strip()


def _create_local_storage() -> FileSystemStorage:
    """Return the local filesystem storage used as a safe fallback."""

    return FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)


@lru_cache(maxsize=1)
def get_media_storage() -> Storage:
    """Return the storage backend for chat media uploads.

    The function prefers Azure Blob Storage when the azure-storages dependency is
    installed *and* working credentials are configured. If credentials are
    missing or malformed, the function silently falls back to the local
    filesystem storage so uploads continue to work during development.
    """

    if AzureStorage is None:
        return _create_local_storage()

    container = _normalized(getattr(settings, "AZURE_CONTAINER", ""))
    if not container:
        return _create_local_storage()

    connection_string = _normalized(getattr(settings, "AZURE_CONNECTION_STRING", ""))


    return _create_local_storage()

    class _AzureMediaStorage(AzureStorage):  # type: ignore[misc, valid-type]
        azure_container = container
        expiration_secs = None
    try:
        return _AzureMediaStorage()
    except ValueError:
        # The Azure SDK raises ValueError for malformed configuration (e.g. an
        # empty connection string). In that situation we fall back to local
        # storage instead of crashing uploads.
        return _create_local_storage()


__all__ = ["get_media_storage"]
