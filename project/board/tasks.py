import time

from .models import Post
from core.celery_app import app as celery_app


@celery_app.task
def reset_post_upvotes():
	posts =Post.upvotes.through.objects.all()
	posts.delete()
	return print("Upvotes cleaned!")
