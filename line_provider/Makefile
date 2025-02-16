DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
EXEC = docker exec -it
DB_CONTAINER = line-postgres-db
LOGS = docker logs
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = line-main-app
PROJECT_NAME = line-provider
MESSAGE_FILE = docker_compose/messaging.yaml

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} up -d --build

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql

.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${MESSAGE_FILE} -p ${PROJECT_NAME} up -d --build

.PHONY: app-logs
app-logs:
	${LOGS} -f ${APP_CONTAINER}

.PHONY: shell
shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate -m "$(name)"

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} alembic upgrade heads

.PHONY: base_downgrade
base_downgrade:
	${EXEC} ${APP_CONTAINER} alembic downgrade base

.PHONY: tests
tests:
	${EXEC} ${APP_CONTAINER} pytest
