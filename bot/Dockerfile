# Dockerfile for bot
FROM python:3.9-slim

WORKDIR /app

COPY bot.py .
RUN pip install aiogram redis

CMD ["python", "bot.py"]
