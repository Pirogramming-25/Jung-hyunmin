# posts/serializers.py
from rest_framework import serializers

from accounts.serializers import UserSummarySerializer

from .models import Comment, Post, PostImage, Story, StoryImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'order']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSummarySerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'parent', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate(self, attrs):
        parent = attrs.get('parent')
        post = attrs.get('post', getattr(self.instance, 'post', None))
        if parent and post and parent.post_id != post.id:
            raise serializers.ValidationError('parent 댓글은 같은 게시글에 속해야 합니다.')
        return attrs


class PostSerializer(serializers.ModelSerializer):
    author = UserSummarySerializer(read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'images', 'caption', 'created_at', 'updated_at',
            'likes_count', 'comments_count', 'is_liked', 'is_bookmarked',
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def _current_user(self):
        request = self.context.get('request')
        return request.user if request else None

    def get_is_liked(self, obj):
        user = self._current_user()
        return bool(user and user.is_authenticated and obj.likes.filter(pk=user.pk).exists())

    def get_is_bookmarked(self, obj):
        user = self._current_user()
        return bool(user and user.is_authenticated and obj.bookmarks.filter(pk=user.pk).exists())


class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, allow_empty=False
    )

    class Meta:
        model = Post
        fields = ['id', 'caption', 'images']
        read_only_fields = ['id']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        post = Post.objects.create(**validated_data)
        PostImage.objects.bulk_create([
            PostImage(post=post, image=image, order=index)
            for index, image in enumerate(images_data)
        ])
        return post


class StoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryImage
        fields = ['id', 'image', 'order']


class StorySerializer(serializers.ModelSerializer):
    author = UserSummarySerializer(read_only=True)
    images = StoryImageSerializer(many=True, read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'author', 'images', 'created_at', 'is_expired']


class StoryCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, allow_empty=False
    )

    class Meta:
        model = Story
        fields = ['id', 'images']
        read_only_fields = ['id']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        story = Story.objects.create(**validated_data)
        StoryImage.objects.bulk_create([
            StoryImage(story=story, image=image, order=index)
            for index, image in enumerate(images_data)
        ])
        return story
