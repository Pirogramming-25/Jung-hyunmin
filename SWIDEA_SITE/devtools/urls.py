from django.urls import path
from . import views

urlpatterns = [
    path('', views.devtool_list, name='devtool-list'),
    path('<int:pk>/', views.devtool_detail, name='devtool-detail'),
    path('<int:pk>/update/', views.devtool_update, name='devtool-update'),
    path('<int:pk>/delete/', views.devtool_delete, name='devtool-delete'),
    path('create/', views.devtool_create, name='devtool-create'),
]