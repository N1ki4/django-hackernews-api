from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    link = models.URLField()
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='upvoted_posts',
        editable=False,
        through='Upvote'
    )

    def __str__(self):
        return self.title


class Upvote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Post: {self.post.title} upvoted by: {self.user}"


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.SET_NULL,
        null=True
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'Comment',
        related_name='children',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.content
