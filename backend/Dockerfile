FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p uploads voice_uploads profile_pics audio

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
