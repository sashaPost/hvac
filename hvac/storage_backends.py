import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class MediaStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs["location"] = os.path.join(settings.MEDIA_ROOT, "images")
        kwargs["base_url"] = os.path.join(settings.MEDIA_URL, "images")
        super().__init__(*args, **kwargs)
