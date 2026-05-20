FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

COPY static templates app.py flag.txt ./

EXPOSE 8080

CMD ["uv", "run", "gunicorn", "--timeout", "5", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]

