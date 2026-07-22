import json
import logging

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

from .services.sentiment import run_sentiment
from .validators import validate_text_input
from .decorators import model_login_required
from .models import InferenceHistory
from .services.summarizer import run_summarize
from .validators import validate_text_input
from .services.moderator import run_moderate

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
@ensure_csrf_cookie
def summarize_view(request):
  histories = (
    InferenceHistory.objects
    .filter(user=request.user, task=InferenceHistory.Task.SUMMARIZE)
    .order_by("-created_at")[:5]
  )
  return render(
    request,
    "my_gpt/summarize.html",
    {"active_tab": "summarize", "histories": histories},
  )

@model_login_required
@require_http_methods(["POST"])
def summarize_run_view(request):
  try:
    body = json.loads(request.body)
  except json.JSONDecodeError:
    return JsonResponse({"error": "잘못된 요청입니다."}, status=400)
  
  text = body.get("text", "")
  
  error = validate_text_input(text, min_length=100, max_length=5000)
  if error:
    return JsonResponse({"error": error}, status=400)
  
  try:
    result = run_summarize(text.strip())
  except Exception:
    logger.exception("Summarize model inference failed.")
    return JsonResponse(
      {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
      status=502,
    )
  
  InferenceHistory.objects.create(
    user = request.user,
    task = InferenceHistory.Task.SUMMARIZE,
    input_text = text.strip(),
    output_text = result["summary"],
    result_data = result,
  )
  return JsonResponse(result)

@model_login_required
@ensure_csrf_cookie
def moderate_view(request):
  histories = (
    InferenceHistory.objects
    .filter(user = request.user, task=InferenceHistory.Task.MODERATE)
    .order_by("-created_at")[:5]
  )
  return render(
    request,
    "my_gpt/moderate.html",
    {"active_tab": "moderate", "histories": histories},
  )

@model_login_required
@require_http_methods(["POST"])
def moderate_run_view(request):
  try:
    body = json.loads(request.body)
  except json.JSONDecodeError:
    return JsonResponse({"error": "잘못된 요청입니다."}, status=400)
  
  text = body.get("text", "")
  
  error = validate_text_input(text, min_length=1, max_length=1000)
  if error:
    return JsonResponse({"error": error}, status=400)
  
  try:
    result = run_moderate(text.strip())
  except Exception:
    logger.exception("Moderate model inference failed.")
    return JsonResponse(
      {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
      status=502,
    )
  
  InferenceHistory.objects.create(
    user = request.user,
    task = InferenceHistory.Task.MODERATE,
    input_text = text.strip(),
    output_text = result["highest_label"],
    result_data = result,
  )
  
  return JsonResponse(result)

def combo_view(request):
  return HttpResponse("combo placeholder")