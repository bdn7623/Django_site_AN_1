from datetime import datetime, date

from django import template

register = template.Library()


@register.filter
def calculate_age(born):
    """
    Custom template filter to calculate the age based on the birth date.

    Args:
    - born: The birth date of the user.

    Returns:
    - int: The age of the user calculated based on the birth date.
    """
    today = date.today()
    birth_date = datetime.strptime(str(born), "%Y-%m-%d").date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


@register.filter
def calculate_days(born):
    """
    Custom template filter to calculate the number of days since the birth date.

    Args:
    - born: The birth date of the user.

    Returns:
    - int: The number of days since the birth date.
    """
    today = date.today()
    birth_date = datetime.strptime(str(born), "%Y-%m-%d").date()
    days = (today - birth_date).days
    return days
