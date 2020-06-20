from rest_framework import serializers

from .models import Post, Comment


class FilterCommentSerializer(serializers.ListSerializer):
    """
    Helper class for filtering spare children comments outside the parent class.
    """

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """
    Helper class for recursive listing comments.
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    children = RecursiveSerializer(many=True, required=False)

    class Meta:
        list_serializer_class = FilterCommentSerializer
        model = Comment
        fields = ("id", "author", "creation_date", "content", "parent", "children")
        read_only_fields = ("id", "author", "creation_date")


class PostSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    comments_count = serializers.SerializerMethodField()
    upvotes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "link",
            "creation_date",
            "author",
            "comments_count",
            "upvotes_count",
        )
        read_only_fields = ('id', "creation_date", "author", "comments_count", "upvotes_count")

    def get_comments_count(self, object):
        return object.comments.count()

    def get_upvotes_count(self, object):
        return object.upvotes.count()


class PostDetailSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    comments_count = serializers.SerializerMethodField()
    upvotes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            "title",
            "link",
            "creation_date",
            "author",
            "comments_count",
            "upvotes_count",
            "comments",
        )

    def get_comments_count(self, object):
        return object.comments.count()

    def get_upvotes_count(self, object):
        return object.upvotes.count()
