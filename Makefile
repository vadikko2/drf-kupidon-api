all: run

# Установка python зависимостей
build:
	@echo "Installing requirements"
	@bash -c "python3.12 -m venv venv"
	@bash -c "cp .env.example .env"
	@bash -c "source ./venv/bin/activate; unset all_proxy; unset ALL_PROXY; pip install --no-cache-dir -r ./requirements.txt --root-user-action=ignore"
	@echo "Please update .env file"

run:
	@echo "Running server"
	@bash -c "export $(grep -v '^#' .env | xargs)"
	@bash -c "docker compose -f docker-compose-dev.yaml up --build -d api"