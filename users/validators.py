from django.core.exceptions import ValidationError
from PIL import Image
import re

# Validation for Profile
def validate_age(value):
    if  value < 8 or value >= 100:
        raise ValidationError("Outside the age group")


def validate_height(value):
    if value < 100 or value > 300:
        raise ValidationError("Outside the height group")


def validate_avatar_size(value):
    max_size_mb = 5
    if value.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image file too large. Maximum size is {max_size_mb}MB.")


def validate_avatar_format(value):
    allowed_formats = ["JPEG", "PNG"]
    try:
        img = Image.open(value)
        if img.format not in allowed_formats:
            raise ValidationError(f"Unsupported image format: {img.format}. Use JPEG or PNG.")
    except Exception:
        raise ValidationError("The uploaded file is not a valid image.")


def validate_phone(value):
    if not re.match(r'^\+380\d{9}$', value):
        raise ValidationError("Enter a valid phone number in the format +380XXXXXXXXX.")



