from django.core.exceptions import ValidationError

def validate_file_size(file):
    """
    Validates is file size is greater than the maximum size
    """
    max_size_in_bytes = 10 * 1024 * 1024  # For max size 10MB

    if file.size > max_size_in_bytes:
        raise ValidationError("File size cannot be greater than 10MB")