# Dockerfile for currency_service
FROM python:3.9-slim

WORKDIR /app

COPY currency_service.py .
RUN pip install aiohttp redis

CMD ["python", "currency_service.py"]
