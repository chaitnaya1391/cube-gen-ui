.PHONY: up down build logs ps restart exec

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

ps:
	docker-compose ps

restart:
	docker-compose restart

exec:
	docker-compose exec db psql -U admin -d spotify
