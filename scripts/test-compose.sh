#!/usr/bin/env bash
set -euo pipefail

echo "Starting SecureBank Docker Compose stack..."
docker compose up -d --build

echo "Running database migrations..."
docker compose exec -T backend flask --app run.py db upgrade

echo "Seeding database..."
docker compose exec -T backend flask --app run.py seed-db

echo "Checking health endpoint..."
curl -f http://localhost:5000/health

echo ""
echo "Checking accounts endpoint..."
curl -f http://localhost:5000/api/accounts

echo ""
echo "Running backend pytest suite inside container..."
docker compose exec -T backend pytest

echo "SecureBank Compose integration checks completed successfully."
