from django import template


register = template.Library()


@register.filter
def is_liked_by(instance, user):
    """
    Check if the instance is liked by the specified user.

    Args:
        instance: The instance to check (e.g., a Post or Comment object).
        user: The user object.

    Returns:
        bool: True if the instance is liked by the user, False otherwise.
    """
    if user.is_authenticated:
        return instance.is_liked_by(user)
    return False


@register.filter
def is_disliked_by(instance, user):
    """
    Check if the instance is disliked by the specified user.

    Args:
        instance: The instance to check (e.g., a Post or Comment object).
        user: The user object.

    Returns:
        bool: True if the instance is disliked by the user, False otherwise.
    """
    if user.is_authenticated:
        return instance.is_disliked_by(user)
    return False
