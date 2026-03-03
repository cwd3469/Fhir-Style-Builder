# Python 3.11 이미지 사용 (3.14는 너무 최신이라 호환성 문제 있을 수 있음)
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 목록 먼저 복사 후 설치 (캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 코드 복사
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
