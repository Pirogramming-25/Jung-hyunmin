# 서비스 소개

Django + Hugging Face `pipeline()`을 활용한 AI 웹 서비스입니다.
감정 분석, 문서 요약, 유해 표현 분석 기능을 제공하며, 로그인 사용자에게는
실행 기록을 저장하고, 세 모델을 체이닝하는 복합 분석 기능도 포함합니다.

## 실행 방법

\`\`\`bash
git clone <repo-url>
cd Django_GPT
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# .env 파일 열어서 DJANGO_SECRET_KEY 등 값 채우기

python manage.py migrate
python manage.py createsuperuser  # 로그인 테스트용 계정 생성

python manage.py runserver
\`\`\`

브라우저에서 http://127.0.0.1:8000/sentiment/ 접속 or http://127.0.0.1:8000/accounts/login/으로 접속해 로그인하면 자동으로 리다이렉트

## 로그인 리다이렉트 동작

비로그인 상태로 로그인이 필요한 페이지(`/summarize/`, `/moderate/`, `/combo/`)에
접속하면 다음과 같이 동작합니다.

1. `/accounts/login/?next=<원래 URL>&required=1`로 자동 리다이렉트
2. 로그인 페이지에서 "로그인 후 이용해주세요" alert 표시
3. 로그인 성공 시 `next` 값을 이용해 **원래 접근하려던 페이지로 자동 복귀**

즉, 사용자가 `/accounts/login/`에 직접 접속해 로그인하는 경우가 아니라
제한된 페이지에 먼저 접근했을 때만 이 리다이렉트 흐름이 트리거되며,
로그인 후 별도 클릭 없이 원래 보려던 페이지로 이동합니다.

## 환경변수 설정 (.env)

| 변수 | 설명 | 필수 여부 |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Django 시크릿 키 | 필수 |
| `DJANGO_DEBUG` | 디버그 모드 (`True`/`False`) | 필수 |
| `HUGGINGFACE_TOKEN` | Hugging Face 토큰 (rate limit 완화용) | 선택 |
> 본 프로젝트에서 사용하는 3개 모델은
> 모두 공개(public) 모델이라 **API 키/토큰 없이도 다운로드 및 실행이 가능합니다.**
## 사용 모델

| 기능 | Model ID | Task | 입력 언어 | 출력 |
| --- | --- | --- | --- | --- |
| 감정 분석 | `cardiffnlp/twitter-roberta-base-sentiment-latest` | text-classification | 영어 | positive / neutral / negative + 신뢰도 |
| 문서 요약 | `sshleifer/distilbart-cnn-6-6` | summarization | 영어 | 요약문 + 원문/요약 길이 + 요약 비율 |
| 유해 표현 분석 | `unitary/toxic-bert` | text-classification (multi-label) | 영어 | toxic / severe_toxic / obscene / threat / insult / identity_hate 각 점수 |

모든 모델은 Hugging Face Hub의 공개(public) 모델이며, 따라서 api키가 필요하지 않습니다.

- cardiffnlp/twitter-roberta-base-sentiment-latest: [모델 카드 링크]
- sshleifer/distilbart-cnn-6-6: [모델 카드 링크]
- unitary/toxic-bert: [모델 카드 링크]

## URL 구조 및 접근 권한

| URL | 기능 | 접근 권한 |
| --- | --- | --- |
| `/sentiment/` | 감정 분석 | 비로그인 허용 |
| `/summarize/` | 문서 요약 | 로그인 필요 |
| `/moderate/` | 유해 표현 분석 | 로그인 필요 |
| `/combo/` | 복합 분석 (챌린지) | 로그인 필요 |

## 주요 구현 사항

- Hugging Face 모델은 `services/` 계층에 분리, `lru_cache`로 Lazy Loading + 캐싱
- CPU / CUDA / Apple Silicon(MPS) 자동 감지 (`services/common.py`)
- 서버 사이드 입력값 검증 (빈 문자열, 공백, 길이, 타입)
- CSRF 보호 적용 (`X-CSRFToken` 헤더 방식, `@csrf_exempt` 미사용)
- 로그인 필요 페이지는 커스텀 데코레이터로 `next`/`required=1` 리다이렉트 처리
- 로그인 사용자의 실행