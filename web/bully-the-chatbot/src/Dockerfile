FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Runtime deps (kept) + build deps (purged later)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgomp1 curl ca-certificates \
        build-essential cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Qwen2.5-0.5B-Instruct Q4_K_M GGUF (~400 MB)
RUN curl -L -o /app/model.gguf \
    https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf

# Strip build tooling to keep image small
RUN apt-get purge -y --auto-remove build-essential cmake \
    && rm -rf /var/lib/apt/lists/*

COPY system_prompt.txt app.py ./
COPY static ./static

ENV MODEL_PATH=/app/model.gguf \
    LLAMA_THREADS=4

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
