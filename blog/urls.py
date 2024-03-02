from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('category/<slug:category>', post_category, name='post_category'),
    path('author/<slug:author>', post_author, name='post_author'),
    path('search/', search_post, name='search_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', like_post, name='post_like'),
    path('post/<int:post_id>/dislike/', dislike_post, name='post_dislike'),
    path('post/<int:post_id>/add_comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/like/', like_comment, name='comment_like'),
    path('comment/<int:comment_id>/dislike/', dislike_comment, name='comment_dislike'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('toggle_comment_active/<int:comment_id>/', toggle_comment_active, name='toggle_comment_active')
]
