from urllib.parse import urlparse

from django.core.exceptions import ValidationError


class YouTubeURLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        parsed_url = urlparse(value)
        if not parsed_url.netloc.endswith("youtube.com"):
            raise ValidationError(
                f"{self.field} должен содержать действительную ссылку на youtube.com"
            )
