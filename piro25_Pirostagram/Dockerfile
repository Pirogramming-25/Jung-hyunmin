FROM python:3.13.7

WORKDIR /app

# 레이어 캐싱으로 인해 먼저 COPY 함
COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# collectstatic 실행 시 settings.py가 SECRET_KEY를 필수로 요구하므로 빌드 전용 더미 값을 사용함
# (이 값은 이미지에 남지 않고, 실행 시에는 --env-file 등으로 진짜 값을 주입해야 함)
ARG DJANGO_SECRET_KEY=build-time-placeholder-key
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD python manage.py migrate --noinput &&\
    python manage.py runserver 0.0.0.0:8000