from django.contrib import admin

from .models import (
    Category,
    Post,
    PostLike,
    PostDislike,
    Comment,
    CommentLike,
    CommentDislike
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin view for Category model.

    Displays name and slug fields in the list view.
    Supports searching by name field.
    Automatically populates the slug field based on the name.
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin view for Post model.

    Displays title, slug, author, publish, and status fields in the list view.
    Supports searching by title and body fields.
    Allows filtering by status and created fields.
    Automatically populates the slug field based on the title.
    Orders the list by status and publish date in descending order.
    Supports selecting the author using a raw ID field.
    """
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    search_fields = ('title', 'body')
    list_filter = ('status', 'created', 'author')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-status', '-publish')
    raw_id_fields = ('author',)


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    """
    Admin view for PostLike model.

    Displays post and user fields in the list view.
    Supports searching by post author's and user's usernames.
    """
    list_display = ('post', 'user')
    search_fields = ('post__author__username', 'user__username')


@admin.register(PostDislike)
class PostDislikeAdmin(admin.ModelAdmin):
    """
    Admin view for PostDislike model.

    Displays post and user fields in the list view.
    Supports searching by post author's and user's usernames.
    """
    list_display = ('post', 'user')
    search_fields = ('post__author__username', 'user__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin view for Comment model.

    Displays post, author, created, and active fields in the list view.
    Allows filtering by active, created, and updated fields.
    Supports searching by author's username and body.
    Provides actions to activate and deactivate comments in bulk.
    """
    list_display = ('post', 'author', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('author__username', 'body')
    actions = ['activate_comments', 'deactivate_comments']

    def activate_comments(self, request, queryset):
        queryset.update(active=True)

    def deactivate_comments(self, request, queryset):
        queryset.update(active=False)


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    """
    Admin view for CommentLike model.

    Displays comment and user fields in the list view.
    Supports searching by comment author's and user's usernames.
    """
    list_display = ('comment', 'user')
    search_fields = ('comment__author__username', 'user__username')


@admin.register(CommentDislike)
class CommentDislikeAdmin(admin.ModelAdmin):
    """
    Admin view for CommentDislike model.

    Displays comment and user fields in the list view.
    Supports searching by comment author's and user's usernames.
    """
    list_display = ('comment', 'user')
    search_fields = ('comment__author__username', 'user__username')
