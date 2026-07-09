"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from accounts.views import (
    CSRFView,
    LoginView,
    LogoutView,
    SignupView,
    login_view,
    profile_view,
    search_view,
    signup_view,
)
from posts.views import (
    create_post_view,
    create_story_view,
    home_view,
    post_detail_view,
    story_detail_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 페이지 (템플릿) 라우트
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('search/', search_view, name='search'),
    path('posts/create/', create_post_view, name='create_post'),
    path('posts/<int:pk>/', post_detail_view, name='post_detail'),
    path('stories/create/', create_story_view, name='create_story'),
    path('stories/<int:pk>/', story_detail_view, name='story_detail'),
    path('profile/<str:username>/', profile_view, name='profile'),

    # API 라우트
    path('api/csrf/',   CSRFView.as_view()),
    path('api/signup/', SignupView.as_view()),
    path('api/login/',  LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/', include('accounts.urls')),
    path('api/', include('posts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
