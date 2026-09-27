FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY extract_videos.py extract_polls.py supabase_engine.py ./

CMD ["sh", "-c", "python ${SCRIPT:-extract_videos.py}"]
