import os

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [
        ".pdf",
        ".doc",
        ".docx",
        ".jpg",
        ".png",
        ".xlsx",
        ".xls",
        ".ppt",
    ]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Invalid File")


# ----------------------- company validator ------------------- #
PhoneNumberValidator = RegexValidator(r"^0[0-9]{10,12}$", "Invalid Phone Number")
ZipCodeValidator = RegexValidator("^(^[0-9]{5}(?:-[0-9]{4})?$|^$)", "Invalid ZIP Code")
