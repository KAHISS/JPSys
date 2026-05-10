# variaveis de ambientr
venv := "env/.env"
main := "src/manage.py"

default:
    @just --list

watch:
    docker compose --env-file {{venv}} up --watch   

build:
    docker compose --env-file {{venv}} up --build

down:
    docker compose down

makemigrations:
    uv run python {{main}} makemigrations

