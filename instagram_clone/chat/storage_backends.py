"""Storage backends used by the chat application."""

from functools import lru_cache
from typing import Optional

from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage

try:
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

    connection_string = _normalized(getattr(settings, "AZURE_CONNECTION_STRING", None))
    account_name = _normalized(getattr(settings, "AZURE_ACCOUNT_NAME", ""))
    account_key = _normalized(getattr(settings, "AZURE_ACCOUNT_KEY", ""))

    has_connection_string = bool(connection_string)
    has_explicit_credentials = bool(account_name and account_key)

    if not (has_connection_string or has_explicit_credentials):
        return _create_local_storage()

    class _AzureMediaStorage(AzureStorage):  # type: ignore[misc, valid-type]
        azure_container = container
        expiration_secs = None

    if has_connection_string:
        _AzureMediaStorage.connection_string = connection_string  # type: ignore[attr-defined]
    else:
        _AzureMediaStorage.account_name = account_name  # type: ignore[attr-defined]
        _AzureMediaStorage.account_key = account_key  # type: ignore[attr-defined]

    try:
        return _AzureMediaStorage()
    except ValueError:
        # The Azure SDK raises ValueError for malformed connection strings. In
        # that situation the safer behaviour is to fall back to the local
        # storage backend instead of crashing the upload flow.
        return _create_local_storage()


__all__ = ["get_media_storage"]
