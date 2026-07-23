def validate_text_input(text, min_length, max_length):
  if not isinstance(text, str):
    return "잘못된 입력입니다."
  
  stripped = text.strip()
  
  if len(stripped) == 0:
    return "빈 문자열은 입력할 수 없습니다."
  
  if len(stripped) < min_length:
    return f"최소 {min_length}자 이상 입력해주세요."
  
  if len(stripped) > max_length:
    return f"최대 {max_length}자 이상 입력해주세요."
  
  return None