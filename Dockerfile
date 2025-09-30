# Dockerfile

# 파이썬 3.11 슬림 버전 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 모든 소스 코드 복사
COPY . /app/

# uvicorn으로 FastAPI 앱 실행 (배포 환경에 적합한 명령)
# main.py의 app 객체를 8000 포트로 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]