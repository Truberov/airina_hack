all:
	@echo "make local-backend - Run backend locally"
	@echo "make logs-backend - Check backend logs"
	@echo "make migrations	- Make migrations"
	@echo "make migrate	    - Migrate db"
	@echo "make env - creates env.local"
	@exit 0

COMPOSE_FILE = docker-compose.local.yml

env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.example .env

local-backend:  ##@Starts locally backend
	docker-compose -f $(COMPOSE_FILE) up --build -d

logs-backend:
	docker-compose -f $(COMPOSE_FILE) logs logs --tail=200 -f lawyer

migrations:
	docker-compose -f $(COMPOSE_FILE) exec lawyer python manage.py makemigrations

migrate:
	docker-compose -f $(COMPOSE_FILE) exec lawyer python manage.py migrate $(args)

django-shell:
	docker-compose -f $(COMPOSE_FILE) exec lawyer python manage.py shell

stop:
	docker-compose -f $(COMPOSE_FILE) stop