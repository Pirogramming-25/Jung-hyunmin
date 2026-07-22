import json
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

from .services.sentiment import run_sentiment
from .validators import validate_text_input
from .decorators import model_login_required

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def sentiment_view(request):
  return render(request, "my_gpt/sentiment.html", {"active_tab": "sentiment"})

@require_http_methods(["POST"])
def sentiment_run_view(request):
  try:
    body = json.loads(request.body)
  except json.JSONDecodeError:
    return JsonResponse({"error": "잘못된 요청입니다."}, status=400)
  
  text = body.get("text", "")
  error = validate_text_input(text, min_length=1, max_length=1000)
  if error:
    return JsonResponse({"error": error}, status=400)
  
  try:
    result = run_sentiment(text.strip())
  except Exception:
    logger.exception("Sentiment model inference failed.")
    return JsonResponse(
      {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
      status=502,
    )
  return JsonResponse(result)

@model_login_required
def summarize_view(request):
  return HttpResponse("summarize placeholder")

def moderate_view(request):
  return HttpResponse("moderate placeholder")

def combo_view(request):
  return HttpResponse("combo placeholder")