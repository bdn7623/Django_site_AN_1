from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    AppConfig for the blog application.

    Attributes:
        default_auto_field (str): The name of the default auto-generated field class for models.
        name (str): The name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
