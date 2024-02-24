from .models import Category, User
from django.db.models import Count


def get_categories(request):
    """
    Retrieve all categories from the database.

    Args:
        request: HttpRequest object representing the current request.

    Returns:
        dict: A dictionary containing all categories retrieved from the database.

    """
    categories = Category.objects.all()
    return {'categories': categories}


def get_author(request):
    """
    Retrieve all authors who have at least one post from the database.

    Args:
        request: HttpRequest object representing the current request.

    Returns:
        dict: A dictionary containing all authors with at least one post retrieved from the database.
    """
    authors = User.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
    return {'authors': authors}
