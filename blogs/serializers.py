from rest_framework import serializers

from blogs.models import Blog, Like, Comment


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('mark', 'owner')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text',)


class BlogSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = Blog
        fields = '__all__'
