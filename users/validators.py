from django.core.exceptions import ValidationError
from PIL import Image
import re


def validate_height(value):
    """Reject unrealistic heights (stored in centimeters)."""
    if value < 100 or value > 300:
        raise ValidationError("Outside the height group")


def validate_avatar_size(value):
    """Reject avatar uploads larger than 5MB to keep media storage in check."""
    max_size_mb = 5
    if value.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image file too large. Maximum size is {max_size_mb}MB.")


def validate_avatar_format(value):
    """Reject anything that isn't actually a JPEG/PNG image.

    We open the file with Pillow instead of trusting the filename
    extension — a renamed file (e.g. malicious.exe -> photo.jpg)
    would otherwise pass a naive extension check.
    """
    allowed_formats = ["JPEG", "PNG"]
    try:
        img = Image.open(value)
        if img.format not in allowed_formats:
            raise ValidationError(f"Unsupported image format: {img.format}. Use JPEG or PNG.")
    except Exception:
        raise ValidationError("The uploaded file is not a valid image.")


def validate_phone(value):
    """Require Ukrainian phone numbers in international format (+380XXXXXXXXX)."""
    if not re.match(r'^\+380\d{9}$', value):
        raise ValidationError("Enter a valid phone number in the format +380XXXXXXXXX.")