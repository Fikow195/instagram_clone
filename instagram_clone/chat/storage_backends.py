"""Storage backends used by the chat application."""

from django.conf import settings
from django.core.files.storage import FileSystemStorage

try:
    from storages.backends.azure_storage import AzureStorage  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    AzureStorage = None  # type: ignore


def _has_valid_azure_settings() -> bool:
    """Return True when Azure storage can be used safely."""

    required_settings = (
        getattr(settings, "AZURE_ACCOUNT_NAME", ""),
        getattr(settings, "AZURE_ACCOUNT_KEY", ""),
        getattr(settings, "AZURE_CONTAINER", ""),
    )
    return all(required_settings) and AzureStorage is not None


if _has_valid_azure_settings():

    class AzureMediaStorage(AzureStorage):
        """Azure-backed storage for chat media files."""

        account_name = settings.AZURE_ACCOUNT_NAME
        account_key = settings.AZURE_ACCOUNT_KEY
        azure_container = settings.AZURE_CONTAINER
        expiration_secs = None

else:

    class AzureMediaStorage(FileSystemStorage):
        """Local fallback storage when Azure is not configured."""

        def __init__(self, *args, **kwargs):
            kwargs.setdefault("location", settings.MEDIA_ROOT)
            kwargs.setdefault("base_url", settings.MEDIA_URL)
            super().__init__(*args, **kwargs)
