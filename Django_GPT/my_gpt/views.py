from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def sentiment_view(request):
  return HttpResponse("sentiment placeholder")

def summarize_view(request):
  return HttpResponse("summarize placeholder")

def moderate_view(request):
  return HttpResponse("moderate placeholder")

def combo_view(request):
  return HttpResponse("combo placeholder")