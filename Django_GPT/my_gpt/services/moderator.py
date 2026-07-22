from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device

@lru_cache(maxsize=1)
def get_moderator_pipeline():
  return pipeline(
    task="text-classification",
    model="unitary/toxic-bert",
    device=get_pipeline_device(),
    top_k=None,
  )

def run_moderate(text: str) -> dict:
  moderator = get_moderator_pipeline()
  results = moderator(text)[0]
  
  results = sorted(results, key=lambda x: x["score"], reverse=True)
  top = results[0]
  
  return {
    "highest_label": top["label"],
    "highest_score": top["score"],
    "all_scores": results,
  }