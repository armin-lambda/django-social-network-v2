from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible

from .base import INVALID_NAMES


def apply_regex(value, regex, message=None):
    RegexValidator(
        regex=regex,
        message=message or f"{value} is invalid",
    )(value)


@deconstructible
class UsernameValidator:
    def __init__(self, invalid_names=INVALID_NAMES):
        self.invalid_names = invalid_names
    
    def __call__(self, value):
        error_msg = f"Enter a valid username"

        apply_regex(
            value,
            r"^[a-z0-9_.]+$",
            error_msg,
        )

        value_lower = value.lower()
        if any(name in value_lower for name in self.invalid_names):
            raise ValidationError(error_msg)
        
        if value.isdigit():
            raise ValidationError(error_msg)
        
        if all(char in '._' for char in value):
            raise ValidationError(error_msg)


@deconstructible
class NameValidator:
    def __init__(self, field_name='Name'):
        self.field_name = field_name

    def __call__(self, value):
        error_msg = f"Enter a valid {self.field_name}"

        apply_regex(
            value,
            r"^[a-zA-Z]+$",
            error_msg,
        )


@deconstructible
class URLValidator:
    def __call__(self, value):
        if not value.startswith('https://'):
            raise ValidationError('URL must start with https://')
