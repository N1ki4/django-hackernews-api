from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import (
    PostDetailSerializer,
    PostSerializer,
    CommentSerializer,
)


class PostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "link": openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def post(self, request):
        '''
         Add a post.
         parameters = title: string, link: url
         Requires user to be logged in, passes it`s id to an author field.
        '''
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        '''
        Get all posts. Do not requires to be authenticated.
        '''
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        '''
        Helper function to manage get post or raise 404.
        Takes pk as post id.
        '''
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """get a single post"""
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def delete(self, request, pk):
        """delete a post"""
        post = Post.objects.get(id=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "link": openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def put(self, request, pk):
        """update a post"""
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpvote(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Add upvote to a post, or delete if already upvoted.
        """
        post = Post.objects.get(id=pk)
        if request.user in post.upvotes.all():
            post.upvotes.remove(request.user)
            post.save()
            return Response({"Success": "Upvote has been deleted."}, status=status.HTTP_201_CREATED)
        post.upvotes.add(request.user)
        post.save()
        return Response({"Success": "Upvote has been added."}, status=status.HTTP_201_CREATED)


class CommentCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "content": openapi.Schema(type=openapi.TYPE_STRING),
                "parent": openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def post(self, request, pk):
        """
        Add comment to a post.
        Requires user to be authenticated.
        Parameters are content of the comment,
        also you can pass parent (id of the comment) parameter to make a reply to a comment.
        """
        post = Post.objects.get(id=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
