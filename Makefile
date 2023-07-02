build:
	docker compose -f "docker-compose.yml" -p "vk-bot" up --build -d

dev:
	uvicorn app:app --reload

start:
	docker compose -p "vk-bot" start

stop:
	docker compose -p "vk-bot" stop

restart: stop start

up:
	docker compose -f "docker-compose.yml" -p "vk-bot" up -d

clean-data:
	docker system prune -a --volumes

make-migration:
	alembic revision --autogenerate

run-migration:
	alembic upgrade head

lint:
	mypy . --exclude=schemas/
