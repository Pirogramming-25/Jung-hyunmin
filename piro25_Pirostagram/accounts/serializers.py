# accounts/serializers.py
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Follow, User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label='비밀번호 확인')

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'name']
        extra_kwargs = {
            'email': {'required': False},
            'name': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password2': '비밀번호가 일치하지 않습니다.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSummarySerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'bio', 'profile_image']

    def get_profile_image(self, obj):
        if not obj.profile_image:
            return None
        request = self.context.get('request')
        url = obj.profile_image.url
        return request.build_absolute_uri(url) if request else url


class UserDetailSerializer(UserSummarySerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta(UserSummarySerializer.Meta):
        fields = UserSummarySerializer.Meta.fields + [
            'followers_count', 'following_count', 'posts_count', 'is_following',
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_posts_count(self, obj):
        return obj.posts.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        if not (user and user.is_authenticated):
            return False
        return Follow.objects.filter(follower=user, following=obj).exists()
