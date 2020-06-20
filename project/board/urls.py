from django.urls import path

from . import views

urlpatterns = [
    path("posts/", views.PostList.as_view(), name="post_list"),
    path("posts/<int:pk>/", views.PostDetail.as_view(), name="single_post"),
    path("posts/<int:pk>/upvote/", views.PostUpvote.as_view(), name="post_upvote"),
    path("posts/<int:pk>/comment/", views.CommentCreate.as_view(), name="comments"),
]
