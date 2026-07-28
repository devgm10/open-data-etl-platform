FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml .

FROM base AS development

RUN pip install --no-cache-dir ".[dev]"

COPY src/ ./src/
COPY tests/ ./tests/

CMD ["python", "-m", "src.main"]


FROM base AS production

RUN pip install --no-cache-dir .

COPY src/ ./src/

CMD ["python", "-m", "src.main"]