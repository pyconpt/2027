PROJECT_NAME=2027

COMPOSE_FILE=docker-compose.local.yml

export COMPOSE_FILE

.PHONY: help up build down start stop prune ps logs shell manage lock sync
default: up

## help	:	Print commands help.
help : Makefile
	@sed -n 's/^##//p' $<

## up	:	Start up containers.
up:
	@echo "Starting up containers for $(PROJECT_NAME)..."
	docker compose up -d --remove-orphans

## build	:	Build python image.
build:
	@echo "Building python image for $(PROJECT_NAME) using $(COMPOSE_FILE)..."
	docker compose build

## down	:	Stop containers.
down: stop

## start	:	Start containers without updating.
start:
	docker compose start

## stop	:	Stop containers.
stop:
	docker compose stop

## prune	:	Remove containers and their volumes.
prune:
	docker compose down -v $(filter-out $@,$(MAKECMDGOALS))

## ps	:	List running containers.
ps:
	docker ps --filter name='$(PROJECT_NAME)*'

## logs	:	Follow container logs.
logs:
	docker compose logs -f $(filter-out $@,$(MAKECMDGOALS))

# This hack allows for exec when an existing container is found, instead of run --rm
CONTAINER=django
EXEC=$(shell docker compose -f $(COMPOSE_FILE) exec $(CONTAINER) ls > /dev/null 2>&1; echo $$?)

ifeq ($(EXEC), 0)
	RUN=exec
else
	RUN=run --rm
endif

## shell	:	Open a shell in the django container.
shell:
	docker compose $(RUN) $(CONTAINER) bash

## manage	:	Run a manage.py command, e.g. `make manage check`.
##		To use "--flag" arguments include them in quotation marks.
manage:
	docker compose $(RUN) $(CONTAINER) python manage.py $(filter-out $@,$(MAKECMDGOALS)) $(subst \,,$(MAKEFLAGS))

## lock	:	Refresh uv.lock from pyproject.toml.
lock:
	docker compose run --rm $(CONTAINER) uv lock

## sync	:	Install missing packages in the container without rebuilding.
sync:
	docker compose run --rm $(CONTAINER) uv sync --locked

# https://stackoverflow.com/a/6273809/1826109
%:
	@:
