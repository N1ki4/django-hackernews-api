from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import (
    PostDetailSerializer,
    PostSerializer,
    CommentSerializer,
)


class PostListView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetailView(APIView):
    def get(self, request, pk):
        """get a single post"""
        post = Post.objects.get(id=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def delete(self, request, pk):
        """delete a post"""
        post = Post.objects.get(id=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        """update a post"""
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                    author=self.request.user,
                    post=post
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpvote(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        if request.user in post.upvotes.all():
            post.upvotes.remove(request.user)
            post.save()
            return Response({"Success": "Upvote has been deleted."}, status=status.HTTP_201_CREATED)
        else:
            post.upvotes.add(request.user)
            post.save()
            return Response({"Success": "Upvote has been added."}, status=status.HTTP_201_CREATED)
