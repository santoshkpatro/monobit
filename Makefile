.PHONY: dev backend frontend manage \
        makemigrations migrate createsuperuser shell \
        collectstatic reset-db \
        test test-cov test-cov-html

dev:
	@trap 'kill 0' SIGINT; \
	uv run python manage.py runserver & \
	pnpm run dev & \
	wait

backend:
	uv run python manage.py runserver

frontend:
	pnpm run dev

manage:
	uv run python manage.py $(cmd)

makemigrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate

createsuperuser:
	uv run python manage.py createsuperuser

shell:
	uv run python manage.py shell

collectstatic:
	uv run python manage.py collectstatic --noinput

reset-db:
	rm -f db.sqlite3
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	uv run python manage.py makemigrations
	uv run python manage.py migrate

test:
	uv run pytest

test-cov:
	uv run pytest --cov=monobit --cov-branch --cov-report=term-missing

test-cov-html:
	uv run pytest --cov=monobit --cov-branch --cov-report=term-missing --cov-report=html