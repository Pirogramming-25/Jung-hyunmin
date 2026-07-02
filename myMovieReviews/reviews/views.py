from django.shortcuts import render
from .models import Review

# Create your views here.
def review_list(request):
  return render(request, 'reviews/review_list.html')
def review_detail(request, pk):
  return render(request, 'reviews/review_detail.html', {'pk': pk})
def review_form(request, pk=None):
  return render(request, 'reviews/review_form.html', {'pk': pk, 'genre_choices': Review.GENRE_CHOICES})