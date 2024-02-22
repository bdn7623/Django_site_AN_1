from .models import Category


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
