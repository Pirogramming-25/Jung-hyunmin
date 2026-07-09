# posts/urls.py
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet, StoryViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')
router.register('stories', StoryViewSet, basename='story')

urlpatterns = router.urls
