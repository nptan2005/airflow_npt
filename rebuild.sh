#!/bin/bash
docker compose down --volumes --remove-orphans
docker rmi -f airflow-nptan:1.0.0
docker builder prune -a -f
docker compose build --no-cache
docker compose up -d