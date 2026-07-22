from .summarizer import run_summarize
from .sentiment import run_sentiment
from .moderator import run_moderate

def run_combo(text: str, do_sample: bool = False) -> dict:
  summary_result = run_summarize(text, do_sample=do_sample)
  summary_text = summary_result["summary"]
  
  sentiment_result = run_sentiment(summary_text)
  moderate_result = run_moderate(summary_text)
  
  sentiment_label = sentiment_result["label"].lower()
  toxicity_score = moderate_result["highest_score"]
  
  if sentiment_label == "negative":
    sentiment_description = "부정적인 평가를 포함합니다."
  else:
    sentiment_description = "강한 부정적 평가는 확인되지 않았습니다."
  
  if toxicity_score >= 0.5:
    toxicity_description = "유해 표현 가능성이 높습니다."
  else:
    toxicity_description = "심각한 유해 표현 가능성은 낮습니다."
  
  verdict = f"{sentiment_description} {toxicity_description}"
  
  return{
    "original_text": text,
    "summary": summary_text,
    "sentiment": {
      "label": sentiment_result["label"],
      "score": sentiment_result["score"]
    },
    "toxicity": {
      "highest_label": moderate_result["highest_label"],
      "highest_score": moderate_result["highest_score"],
      "all_scores": moderate_result["all_scores"],
    },
    "verdict": verdict,
  }