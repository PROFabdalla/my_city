from django.core.validators import RegexValidator

# ----------------------- company validator ------------------- #
PhoneNumberValidator = RegexValidator(r"^0[0-9]{10,12}$", "Invalid Phone Number")
ZipCodeValidator = RegexValidator("^(^[0-9]{5}(?:-[0-9]{4})?$|^$)", "Invalid ZIP Code")
