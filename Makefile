DC=docker compose

.PHONY: up down build migrate makemigrations createsuperuser shell logs seed

up:
	$(DC) up -d web worker beat

down:
	$(DC) down

build:
	$(DC) build

migrate:
	$(DC) exec web python manage.py migrate

makemigrations:
	$(DC) exec web python manage.py makemigrations

createsuperuser:
	$(DC) exec web python manage.py createsuperuser

shell:
	$(DC) exec web python manage.py shell

logs:
	$(DC) logs -f web worker beat

seed:
	$(DC) exec web python manage.py seed_demo_data --force
