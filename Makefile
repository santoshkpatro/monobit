.PHONY: dev backend frontend test test-cov test-cov-html

dev:
	@echo "Starting backend (uv) and frontend..."
	@trap 'kill 0' SIGINT; \
	uv run python manage.py runserver & \
	pnpm run dev & \
	wait

backend:
	uv run python manage.py runserver

frontend:
	pnpm run dev

test:
	uv run pytest

test-cov:
	uv run pytest --cov=monobit --cov-branch --cov-report=term-missing

test-cov-html:
	uv run pytest --cov=monobit --cov-branch --cov-report=term-missing --cov-report=html
	@echo "Open htmlcov/index.html in your browser"