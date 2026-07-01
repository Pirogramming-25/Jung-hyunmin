from django.urls import path
from . import views
from  .api_views import ReviewListAPI, ReviewDetailAPI

urlpatterns = [
  path('api/reviews/', ReviewListAPI.as_view(), name='api-review-list'),
  path('api/reviews/<int:pk>/', ReviewDetailAPI.as_view(), name='api-review-detail'),
  path('review/', views.review_list, name='review-list'),
  path('review/<int:pk>/', views.review_detail, name='review-detail'),
  path('review/create/', views.review_form, name='review-create'),
  path('review/<int:pk>/update/', views.review_form, name='review-update'),
]