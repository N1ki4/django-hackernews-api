from django.urls import path

from . import views


urlpatterns = [
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="single_post"),
    path("posts/<int:pk>/upvote/", views.PostUpvote.as_view(), name="post_upvote"),
    path("posts/<int:pk>/comments/", views.CommentCreateView.as_view(), name="comment_create"),
]
