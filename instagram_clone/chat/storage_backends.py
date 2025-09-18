"""Storage backends used by the chat application."""

from django.conf import settings
from django.core.files.storage import FileSystemStorage

try:
    from storages.backends.azure_storage import AzureStorage  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    AzureStorage = None  # type: ignore


def _has_valid_azure_settings() -> bool:
    """Return True when Azure storage can be used safely."""

    if AzureStorage is None:
        return False

    container = getattr(settings, "AZURE_CONTAINER", "")
    if not container:
        return False

    connection_string = getattr(settings, "AZURE_CONNECTION_STRING", None)
    account_name = getattr(settings, "AZURE_ACCOUNT_NAME", "")
    account_key = getattr(settings, "AZURE_ACCOUNT_KEY", "")

    has_explicit_credentials = account_name and account_key
    has_connection_string = bool(connection_string)

    return has_connection_string or has_explicit_credentials


if _has_valid_azure_settings():

    class AzureMediaStorage(AzureStorage):
        """Azure-backed storage for chat media files."""

        account_name = settings.AZURE_ACCOUNT_NAME
        account_key = settings.AZURE_ACCOUNT_KEY
        azure_container = settings.AZURE_CONTAINER
        expiration_secs = None

        if settings.AZURE_CONNECTION_STRING:
            # Only expose the connection string when it's provided. Passing an
            # empty value down to the Azure SDK triggers ``ValueError: Connection
            # string is either blank or malformed`` when uploads are attempted.
            connection_string = settings.AZURE_CONNECTION_STRING

else:

    class AzureMediaStorage(FileSystemStorage):
        """Local fallback storage when Azure is not configured."""

        def __init__(self, *args, **kwargs):
            kwargs.setdefault("location", settings.MEDIA_ROOT)
            kwargs.setdefault("base_url", settings.MEDIA_URL)
            super().__init__(*args, **kwargs)
