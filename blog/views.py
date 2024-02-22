from django.shortcuts import render

from .models import Post
from .utils import paginate_objects


def post_list(request):
    objects = Post.published.all()
    posts = paginate_objects(request, objects)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_category(request, category):
    objects = Post.published.filter(category__slug=category)
    posts = paginate_objects(request, objects)
    return render(request, 'blog/post/list.html', {'posts': posts})

