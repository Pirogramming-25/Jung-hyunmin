# accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow, User
from .serializers import SignupSerializer, UserDetailSerializer, UserSummarySerializer


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'signup.html')


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_own_profile = request.user.is_authenticated and request.user.id == profile_user.id

    is_following = False
    if request.user.is_authenticated and not is_own_profile:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    tab = request.GET.get('tab', 'posts')
    if tab == 'bookmarks' and is_own_profile:
        posts_qs = profile_user.bookmarked_posts.select_related('author').prefetch_related('images').order_by('-created_at')
    else:
        tab = 'posts'
        posts_qs = profile_user.posts.select_related('author').prefetch_related('images').order_by('-created_at')

    posts = []
    for post in posts_qs:
        images = list(post.images.all())
        posts.append({'obj': post, 'thumbnail': images[0] if images else None})

    context = {
        'profile_user': profile_user,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'posts_count': profile_user.posts.count(),
        'followers_count': profile_user.followers.count(),
        'following_count': profile_user.following.count(),
        'posts': posts,
        'tab': tab,
    }
    return render(request, 'profile.html', context)


def search_view(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        queryset = User.objects.filter(Q(username__icontains=query) | Q(name__icontains=query))
        if request.user.is_authenticated:
            queryset = queryset.exclude(id=request.user.id)
        results = queryset.order_by('username')[:20]

    following_ids = set()
    if request.user.is_authenticated:
        following_ids = set(request.user.following.values_list('id', flat=True))

    context = {'query': query, 'results': results, 'following_ids': following_ids}
    return render(request, 'search.html', context)


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)   # 가입과 동시에 로그인 처리
        return Response(
            UserSummarySerializer(user, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({'detail': 'CSRF cookie set'})


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'error': '아이디 또는 비밀번호가 올바르지 않습니다.'},
                            status=status.HTTP_400_BAD_REQUEST)
        login(request, user)   # 세션에 유저를 기록 → 응답에 sessionid 쿠키가 실림
        return Response(UserSummarySerializer(user, context={'request': request}).data)


class LogoutView(APIView):
    def post(self, request):
        logout(request)        # 세션 삭제
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSummarySerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, username=None):
        target = self.get_object()
        if target == request.user:
            return Response({'detail': '자기 자신은 팔로우할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            follow.delete()
        return Response({'following': created, 'followers_count': target.followers.count()})

    @action(detail=True, methods=['get'])
    def followers(self, request, username=None):
        user = self.get_object()
        queryset = user.followers.all().order_by('id')
        page = self.paginate_queryset(queryset)
        serializer = UserSummarySerializer(page if page is not None else queryset, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, username=None):
        user = self.get_object()
        queryset = user.following.all().order_by('id')
        page = self.paginate_queryset(queryset)
        serializer = UserSummarySerializer(page if page is not None else queryset, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)