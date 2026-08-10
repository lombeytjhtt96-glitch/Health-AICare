#!/bin/bash
cd /mnt/c/Users/Asus/Downloads/HealthAICare-main2/backend

# Set DATABASE_URL to use local socket
export DATABASE_URL="postgresql+psycopg://postgres:postgres@127.0.0.1:5432/aicare_db"

# Run alembic from venv
./venv/Scripts/python.exe -m alembic upgrade head 2>&1
