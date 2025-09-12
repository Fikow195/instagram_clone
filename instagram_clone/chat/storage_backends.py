from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = "stoga4"
    account_key = "bVBakeCt8U4PA4R02dvCULtdUu8ttR/KGYRmgDwMMzxOe4rDrEWqDbsg1UMjwDVY5DljFOIzAbpx+AStD0ISUg=="
    azure_container = "media"
    expiration_secs = None
