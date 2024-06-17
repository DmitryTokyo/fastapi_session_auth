#!/bin/bash

docker-compose down -v
echo "Starting application and database containers..."
docker-compose up --build -d

