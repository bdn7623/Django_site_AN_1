from django.db import models


class PostPublishedManager(models.Manager):
    """
    Manager for retrieving published posts.
    """

    def get_queryset(self):
        """
        Return queryset containing only published posts.
        """
        return super(PostPublishedManager, self).get_queryset().filter(status='published')
