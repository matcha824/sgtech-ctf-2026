FROM python:3.12-slim

ENV HOST=0.0.0.0
ENV PORT=8080
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && chown appuser:appuser /app

COPY --chown=appuser:appuser app.py ./
COPY --chown=appuser:appuser static ./static

USER appuser

EXPOSE 8080

CMD ["python", "app.py"]
