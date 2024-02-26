import re
from rest_framework import serializers


class YoutubeLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not re.match(r'^https?://(www\.)?youtube\.com/', value):
            raise serializers.ValidationError("Only YouTube links are allowed.")
