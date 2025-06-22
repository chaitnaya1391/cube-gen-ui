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

mcp-build:
	docker compose build mcp

mcp-run:
	docker compose run --rm mcp

reset:
	docker compose down
	docker compose build
	docker compose up -d