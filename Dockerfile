FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:/root/.local/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && corepack enable

RUN pip install uv

COPY . .

RUN uv venv && uv sync --frozen --no-dev

RUN pnpm install --frozen-lockfile && pnpm build

RUN uv run python manage.py collectstatic --noinput

CMD sh -c "uv run python manage.py migrate && uv run gunicorn monobit.wsgi:application --bind 0.0.0.0:$PORT"
