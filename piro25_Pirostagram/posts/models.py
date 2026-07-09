# posts/models.py
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

STORY_LIFETIME = timedelta(hours=24)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Like', related_name='liked_posts')
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Bookmark', related_name='bookmarked_posts')

    class Meta:
        ordering = ['-created_at']

class PostImage(models.Model):
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')
    order = models.PositiveIntegerField(default=0)   # 캐러셀 순서

    class Meta:
        ordering = ['order']

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'post'], name='unique_like')]

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'post'], name='unique_bookmark')]

class Comment(models.Model):
    post   = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StoryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(created_at__gte=timezone.now() - STORY_LIFETIME)


class Story(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)
    # 만료는 created_at 기준으로 조회 시 필터링 (STORY_LIFETIME = 24시간)

    objects = StoryQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    @property
    def is_expired(self):
        return timezone.now() - self.created_at > STORY_LIFETIME

class StoryImage(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='stories/')
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order']