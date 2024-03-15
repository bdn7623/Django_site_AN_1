from datetime import date
from django.core.exceptions import ValidationError

def validate_birth_date(birth):
    """
    Validator function for birth date field.

    Ensures that the birth date meets the following criteria:
    - The year must be greater than 1900.
    - The age must be at least 18 years old.

    Args:
    - birth (date): The birth date to validate.

    Raises:
    - ValidationError: If the birth year is less than 1900 or the age is less than 18.

    Returns:
    - None: If the birth date is valid.
    """
    if birth.year < 1900:
        raise ValidationError('Invalid birth date - year must be greater than 1900.')
    age = (date.today() - birth).days // 365
    if age < 18:
        raise ValidationError('Invalid birth date - your age must be at least 18 years old.')
