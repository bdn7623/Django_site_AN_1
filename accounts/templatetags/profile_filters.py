from datetime import datetime, date

from django import template

register = template.Library()


@register.filter
def calculate_age(born):
    today = date.today()
    birth_date = datetime.strptime(str(born), "%Y-%m-%d").date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


@register.filter
def calculate_days(born):
    today = date.today()
    birth_date = datetime.strptime(str(born), "%Y-%m-%d").date()
    days = (today - birth_date).days
    return days