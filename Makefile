.PHONY: up down build logs ps restart exec mcp-run mcp-build

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

ps:
	docker compose ps

restart:
	docker compose restart

exec:
	docker compose exec db psql -U cubepostgres -d titanic

reset-mcp:
	docker compose down mcp
	docker compose build mcp
	docker compose up -d mcp

reset-adk:
	docker compose down adk
	docker compose build adk
	docker compose up -d adk


reset:
	docker compose down
	docker compose build
	docker compose up -d