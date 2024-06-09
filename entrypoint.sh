#!/bin/bash

source /app/.envrc

exec poetry run uvicorn src.server:app --reload --host 0.0.0.0 --port 5000
