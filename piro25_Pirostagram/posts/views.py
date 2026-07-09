# posts/views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Bookmark, Comment, Like, Post, Story
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    PostCreateSerializer,
    PostSerializer,
    StoryCreateSerializer,
    StorySerializer,
)

User = get_user_model()


@login_required(login_url='login')
def create_post_view(request):
    return render(request, 'create_post.html')


@login_required(login_url='login')
def create_story_view(request):
    return render(request, 'create_story.html')


def post_detail_view(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related('images'), pk=pk
    )
    images = list(post.images.all())

    is_liked = is_bookmarked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(id=request.user.id).exists()
        is_bookmarked = post.bookmarks.filter(id=request.user.id).exists()

    comments = post.comments.select_related('author').order_by('created_at')

    context = {
        'post': post,
        'thumbnail': images[0] if images else None,
        'is_liked': is_liked,
        'is_bookmarked': is_bookmarked,
        'likes_count': post.likes.count(),
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)


def story_detail_view(request, pk):
    story = get_object_or_404(
        Story.objects.select_related('author').prefetch_related('images'), pk=pk
    )
    images = list(story.images.all())
    context = {
        'story': story,
        'images': images,
        'is_own_story': request.user.is_authenticated and request.user.id == story.author_id,
    }
    return render(request, 'story_detail.html', context)


def home_view(request):
    sort = request.GET.get('sort', 'latest')

    if request.user.is_authenticated:
        following_ids = set(request.user.following.values_list('id', flat=True))
        feed_author_ids = following_ids | {request.user.id}
        posts_qs = Post.objects.filter(author_id__in=feed_author_ids)
    else:
        following_ids = set()
        posts_qs = Post.objects.none()

    posts_qs = posts_qs.select_related('author').prefetch_related('images')
    if sort == 'likes':
        posts_qs = posts_qs.annotate(_likes_count=Count('likes', distinct=True)).order_by('-_likes_count', '-created_at')
    else:
        sort = 'latest'
        posts_qs = posts_qs.order_by('-created_at')

    liked_ids, bookmarked_ids = set(), set()
    if request.user.is_authenticated:
        liked_ids = set(request.user.liked_posts.values_list('id', flat=True))
        bookmarked_ids = set(request.user.bookmarked_posts.values_list('id', flat=True))

    posts = []
    for post in posts_qs:
        images = list(post.images.all())
        posts.append({
            'obj': post,
            'thumbnail': images[0] if images else None,
            'is_liked': post.id in liked_ids,
            'is_bookmarked': post.id in bookmarked_ids,
            'is_following_author': post.author_id in following_ids,
            'likes_count': post.likes.count(),
            'comments_count': post.comments.count(),
        })

    if request.user.is_authenticated:
        active_stories = (
            Story.objects.active()
            .filter(author_id__in=following_ids | {request.user.id})
            .select_related('author')
            .prefetch_related('images')
            .order_by('author_id', '-created_at')
        )
    else:
        active_stories = Story.objects.none()

    seen_authors = set()
    stories = []
    for story in active_stories:
        if story.author_id in seen_authors:
            continue
        seen_authors.add(story.author_id)
        images = list(story.images.all())
        story.thumbnail = images[0] if images else None
        stories.append(story)
    stories.sort(key=lambda s: s.created_at, reverse=True)

    if request.user.is_authenticated:
        recommended_users = User.objects.exclude(id__in=list(following_ids) + [request.user.id]).order_by('?')[:4]
    else:
        recommended_users = User.objects.order_by('?')[:4]

    context = {
        'posts': posts,
        'stories': stories,
        'sort': sort,
        'recommended_users': recommended_users,
    }
    return render(request, 'index.html', context)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('images')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
        return Response({'liked': created, 'likes_count': post.likes.count()})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def bookmark(self, request, pk=None):
        post = self.get_object()
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
        if not created:
            bookmark.delete()
        return Response({'bookmarked': created})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all().select_related('author', 'post')
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class StoryViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return StoryCreateSerializer
        return StorySerializer

    def get_queryset(self):
        queryset = Story.objects.all().select_related('author').prefetch_related('images')
        if self.action == 'list':
            queryset = queryset.active()
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
