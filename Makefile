.PHONY: dev backend frontend

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