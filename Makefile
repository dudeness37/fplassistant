.PHONY: up down logs api fe

up:
\tcd infra && docker compose up --build

down:
\tcd infra && docker compose down -v

logs:
\tcd infra && docker compose logs -f

api:
\tcd infra && docker compose exec api bash

fe:
\tcd infra && docker compose exec frontend sh