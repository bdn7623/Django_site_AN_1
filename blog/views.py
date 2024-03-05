import re

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils.text import slugify

from .models import Post, PostLike, PostDislike, Comment, CommentLike, CommentDislike
from .utils import paginate_objects
from .forms import CommentForm, PostForm


def post_list(request):
    """
    Render a list of all published posts.

    Args:
        request: HttpRequest object representing the current request.

    Returns:
        HttpResponse: Rendered HTML response containing the list of posts.
    """
    objects = Post.published.all()
    posts = paginate_objects(request, objects)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post_slug):
    """
    Render details of a specific post.

    Args:
        request: HttpRequest object representing the current request.
        year (int): Year of the post's publication.
        month (int): Month of the post's publication.
        day (int): Day of the post's publication.
        post_slug (str): Slug of the post.

    Returns:
        HttpResponse: Rendered HTML response containing the details of the post.
    """
    post = get_object_or_404(Post,
                             slug=post_slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'form': form})


@login_required
def add_post(request):
    """
    View function to add a new post.

    Args:
        request: HttpRequest object representing the current request.

    Returns:
        HttpResponse: Rendered HTML response containing the form for adding a new post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            return redirect(post.get_absolute_url())

    form = PostForm()
    return render(request, 'blog/post/create.html', {'form': form})


@login_required
def update_post(request, post_id):
    """
    View function to update an existing post.

    Args:
        request: HttpRequest object representing the current request.
        post_id (int): ID of the post to be updated.

    Returns:
        HttpResponse: Rendered HTML response containing the form for updating the post.
    """
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return HttpResponseForbidden("You don't have permission to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            return redirect(post.get_absolute_url())

    form = PostForm(instance=post)
    return render(request, 'blog/post/update.html', {'form': form})


@login_required
def delete_post(request, post_id):
    """
    View function to delete an existing post.

    Args:
        request: HttpRequest object representing the current request.
        post_id (int): ID of the post to be deleted.

    Returns:
        HttpResponse: Redirect response to the post list page after deletion.
    """
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return HttpResponseForbidden("You don't have permission to delete this post.")

    post.delete()
    return redirect('blog:post_list')


def post_category(request, category):
    """
    Render a list of posts filtered by category.

    Args:
        request: HttpRequest object representing the current request.
        category (str): Slug of the category to filter by.

    Returns:
        HttpResponse: Rendered HTML response containing the filtered list of posts.
    """
    objects = Post.published.filter(category__slug=category)
    posts = paginate_objects(request, objects)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_author(request, author):
    """
    Render a list of posts filtered by author.

    Args:
        request: HttpRequest object representing the current request.
        author (str): Username of the author to filter by.

    Returns:
        HttpResponse: Rendered HTML response containing the filtered list of posts.
    """
    objects = Post.published.filter(author__username=author)
    posts = paginate_objects(request, objects)
    return render(request, 'blog/post/list.html', {'posts': posts})


def search_post(request):
    """
    Search posts based on user input.

    Args:
        request: HttpRequest object representing the current request.

    Returns:
        HttpResponse: Rendered HTML response containing the search results.
    """
    search_query = request.GET.get('search_query')
    search_param = request.GET.get('search_param')
    posts = Post.published.all()

    if search_query:
        if search_param == 'author':
            posts = posts.filter(author__username__icontains=search_query)
        elif search_param == 'title':
            posts = posts.filter(title__icontains=search_query)
        elif search_param == 'post':
            posts = posts.filter(
                Q(title__icontains=search_query) | Q(body__icontains=search_query)
            )

        elif search_param == 'publish':
            parts = re.split(r'\W', search_query)
            year = parts[0]
            month = parts[1] if len(parts) > 1 else None
            day = parts[2] if len(parts) > 2 else None

            if month and day:
                posts = posts.filter(publish__year=year, publish__month=month, publish__day=day)
            elif month:
                posts = posts.filter(publish__year=year, publish__month=month)
            else:
                posts = posts.filter(publish__year=year)

    posts = paginate_objects(request, posts)
    return render(request, 'blog/post/list.html', {'posts': posts})


@login_required
def like_post(request, post_id):
    """
    Like a post.

    Args:
        request: HttpRequest object representing the current request.
        post_id (int): ID of the post to like.

    Returns:
        HttpResponseRedirect: Redirects to the detail page of the liked post.
    """
    post = get_object_or_404(Post, id=post_id)

    if post.is_liked_by(request.user):
        like = post.likes.get(user=request.user)
        like.delete()
    else:
        PostLike.objects.create(post=post, user=request.user)
        if post.is_disliked_by(request.user):
            dislike = post.dislikes.get(user=request.user)
            dislike.delete()
    return HttpResponseRedirect(f'{post.get_absolute_url()}#postlikeDislike')


@login_required
def dislike_post(request, post_id):
    """
    Dislike a post.

    Args:
        request: HttpRequest object representing the current request.
        post_id (int): ID of the post to dislike.

    Returns:
        HttpResponseRedirect: Redirects to the detail page of the disliked post.
    """
    post = get_object_or_404(Post, id=post_id)

    if post.is_disliked_by(request.user):
        dislike = post.dislikes.get(user=request.user)
        dislike.delete()
    else:
        PostDislike.objects.create(post=post, user=request.user)
        if post.is_liked_by(request.user):
            like = post.likes.get(user=request.user)
            like.delete()
    return HttpResponseRedirect(f'{post.get_absolute_url()}#postlikeDislike')


@login_required
def add_comment(request, post_id):
    """
    Add a comment to a post.

    Args:
        request: HttpRequest object representing the current request.
        post_id (int): ID of the post to add the comment to.

    Returns:
        HttpResponseRedirect: Redirects to the detail page of the post with the new comment.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
    return HttpResponseRedirect(f'{post.get_absolute_url()}#comments')


@login_required
def like_comment(request, comment_id):
    """
    View function to like a comment.

    Args:
        request: HttpRequest object representing the current request.
        comment_id (int): ID of the comment to be liked.

    Returns:
        HttpResponseRedirect: Redirects to the post detail page with the comment anchor.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.is_liked_by(request.user):
        like = comment.likes.get(user=request.user)
        like.delete()
    else:
        CommentLike.objects.create(comment=comment, user=request.user)
        if comment.is_disliked_by(request.user):
            dislike = comment.dislikes.get(user=request.user)
            dislike.delete()
    return HttpResponseRedirect(f'{comment.post.get_absolute_url()}#commentLike{comment.id}')


@login_required
def dislike_comment(request, comment_id):
    """
    View function to dislike a comment.

    Args:
        request: HttpRequest object representing the current request.
        comment_id (int): ID of the comment to be disliked.

    Returns:
        HttpResponseRedirect: Redirects to the post detail page with the comment anchor.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.is_disliked_by(request.user):
        dislike = comment.dislikes.get(user=request.user)
        dislike.delete()
    else:
        CommentDislike.objects.create(comment=comment, user=request.user)
        if comment.is_liked_by(request.user):
            like = comment.likes.get(user=request.user)
            like.delete()
    return HttpResponseRedirect(f'{comment.post.get_absolute_url()}#commentLike{comment.id}')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_comment(request, comment_id):
    """
    View function to delete a comment.

    Args:
        request: HttpRequest object representing the current request.
        comment_id (int): ID of the comment to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the post detail page with the comments anchor.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return HttpResponseRedirect(f'{comment.post.get_absolute_url()}#comments')
"""
@login_required
def toggle_comment_active(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or comment.usr.is_superuser:
        comment.save()
    return HttpResponseRedirect(f'{comment.post.get_absolute_url()}#comments')
"""


@login_required
@user_passes_test(lambda user: user.is_superuser)
def toggle_comment_active(request, comment_id):
    """
    View function to toggle the active status of a comment.

    Args:
        request: HttpRequest object representing the current request.
        comment_id (int): ID of the comment to toggle its active status.

    Returns:
        HttpResponseRedirect: Redirects to the post detail page with the comments anchor.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.active = not comment.active
    comment.save()
    return HttpResponseRedirect(f'{comment.post.get_absolute_url()}#comments')