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
    creation_date = models.DateTimeField(auto_now_add=True)
    link = models.URLField()
    title = models.CharField(max_length=256)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Upvote'
    )

    def __str__(self):
        return self.title


class Upvote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='upvotes', on_delete=models.CASCADE)


class Comment(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
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
        'self', on_delete=models.CASCADE,
        blank=True, null=True, related_name="children"
    )
    content = models.TextField()

    def __str__(self):
        return self.content
