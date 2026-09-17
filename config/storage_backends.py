from django.conf import settings
from django.core.files.storage import default_storage


def persistent_media_storage():
    # A callable, not a live instance - Django's migration serializer
    # records a reference to this function rather than trying to freeze
    # a storage object into a migration file (this is why it must stay
    # a module-level function, not a lambda or a nested def).
    #
    # Falls back to Django's normal default storage (local disk) when
    # no object-storage credentials are configured, so local
    # development and any environment without them are unaffected.
    if not getattr(settings, 'PERSISTENT_MEDIA_STORAGE_CONFIGURED', False):
        return default_storage

    from storages.backends.s3boto3 import S3Boto3Storage
    return S3Boto3Storage()
