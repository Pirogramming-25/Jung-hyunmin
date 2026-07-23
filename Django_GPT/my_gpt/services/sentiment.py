from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device

@lru_cache(maxsize=1)
def get_sentiment_pipeline():
  return pipeline(
    task="text-classification",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    device=get_pipeline_device(),
    top_k = None,
  )
  
def run_sentiment(text: str) -> dict:
  classifier = get_sentiment_pipeline()
  results = classifier(text)[0]
  
  results = sorted(results, key=lambda x: x["score"], reverse=True)
  
  top = results[0]
  return {
    "label": top["label"],
    "score": top["score"],
    "all_scores": results,
  }