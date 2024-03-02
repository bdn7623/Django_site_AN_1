from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from .managers import PostPublishedManager


class Category(models.Model):
    """
    Model representing a post category.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Model representing a blog post.
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    body = models.TextField(verbose_name='Content')
    publish = models.DateTimeField(default=timezone.localtime)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=255)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='posts')
    objects = models.Manager()
    published = PostPublishedManager()

    class Meta:
        ordering = ('-publish', '-created')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def is_disliked_by(self, user):
        return self.dislikes.filter(user=user).exists()


class PostLike(models.Model):
    """
    Model representing a like on a blog post.
    """
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='likes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='post_likes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')


class PostDislike(models.Model):
    """
    Model representing a dislike on a blog post.
    """
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='dislikes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='post_dislikes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')


class Comment(models.Model):
    """
    Model representing a comment on a blog post.
    """
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='post_comment')
    body = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-updated', '-created')

    def __str__(self):
        return f'{self.author} - {self.post.title}'

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def is_disliked_by(self, user):
        return self.dislikes.filter(user=user).exists()


class CommentLike(models.Model):
    """
    Model representing a like on a comment.
    """
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                related_name='likes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments_likes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')


class CommentDislike(models.Model):
    """
    Model representing a dislike on a comment.
    """
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                related_name='dislikes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments_dislikes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')
