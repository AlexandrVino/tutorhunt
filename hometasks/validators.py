from django.core.exceptions import ValidationError


def file_size(value):
    limit = 4 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 2 MiB.")
