# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # username / password / email 등은 AbstractUser에서 상속받음
    name = models.CharField(max_length=50, blank=True)      # 검색용 실명
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True)

    following = models.ManyToManyField(
        'self',
        through='Follow',
        through_fields=('follower', 'following'),
        related_name='followers',
        symmetrical=False,
    )

class Follow(models.Model):
    follower  = models.ForeignKey('User', on_delete=models.CASCADE, related_name='+')
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow'),
            models.CheckConstraint(condition=~models.Q(follower=models.F('following')), name='no_self_follow'),
        ]