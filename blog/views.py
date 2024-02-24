from django.shortcuts import render
from django.db.models import Q

from .models import Post
from .utils import paginate_objects


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
    Render a list of posts filtered by search query.

    Args:
        request: HttpRequest object representing the current request.

    Returns:
        HttpResponse: Rendered HTML response containing the filtered list of posts.
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
    posts = paginate_objects(request, posts)
    return render(request, 'blog/post/list.html', {'posts': posts})
