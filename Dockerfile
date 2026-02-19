FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    curl nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Enable pnpm
RUN corepack enable

# Install uv
RUN pip install uv

# Copy project
COPY . .

# Install frontend deps & build
RUN pnpm install --frozen-lockfile
RUN pnpm build

# Install python deps
RUN uv sync --frozen --no-dev

# Collect static
RUN uv run python manage.py collectstatic --noinput

CMD uv run gunicorn monobit.wsgi:application --bind 0.0.0.0:$PORT
