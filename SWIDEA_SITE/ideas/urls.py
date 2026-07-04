from django.urls import path
from . import views

urlpatterns = [
    path('', views.idea_list, name='idea-list'),
    path('<int:pk>/', views.idea_detail, name='idea-detail'),
    path('<int:pk>/update/', views.idea_update, name='idea-update'),
    path('<int:pk>/delete/', views.idea_delete, name='idea-delete'),
    path('<int:pk>/star/', views.idea_star_toggle, name='idea-star-toggle'),
    path('<int:pk>/interest/', views.idea_interest_update, name='idea-interest-update'),
    path('create/', views.idea_create, name='idea-create'),
]
