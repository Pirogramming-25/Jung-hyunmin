from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device

@lru_cache(maxsize=1)
def get_summarizer_pipeline():
  return pipeline(
    task="summarization",
    model="sshleifer/distilbart-cnn-6-6",
    device=get_pipeline_device(),
  )

def run_summarize(text: str, do_sample: bool = False) -> dict:
  summarizer = get_summarizer_pipeline()
  
  result = summarizer(
    text,
    max_length=180,
    min_length=40,
    do_sample=do_sample, #기본은 false, 재생성 누르면 True
    **({"top_p": 0.9, "temperature": 0.8} if do_sample else {}),
  )
  
  summary = result[0]["summary_text"]
  
  original_len = len(text)
  summary_len = len(summary)
  ratio = (summary_len/original_len) * 100 if original_len else 0
  
  return {
    "summary": summary,
    "original_length": original_len,
    "summary_length": summary_len,
    "summary_ratio": round(ratio, 2),
  }