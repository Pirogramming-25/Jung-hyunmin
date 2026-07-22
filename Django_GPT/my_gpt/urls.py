from django.urls import path
from . import views

app_name = "my_gpt"

urlpatterns = [
    path("sentiment/", views.sentiment_view, name="sentiment"),
    path("sentiment/run/", views.sentiment_run_view, name="sentiment_run"),
    
    path("summarize/", views.summarize_view, name="summarize"),
    path('summarize/run/', views.summarize_run_view, name="summarize_run"),
    
    path("moderate/", views.moderate_view, name="moderate"),
    path("moderate/run/", views.moderate_run_view, name="moderate_run"),
    
    path("combo/", views.combo_view, name="combo"),
]
