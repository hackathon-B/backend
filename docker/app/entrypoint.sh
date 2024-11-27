#!/bin/sh

# データベースが起動するまで待機
echo "Waiting for database to be ready..."
while ! nc -z db 3306; do
  sleep 1
done
echo "Database is ready!"

# マイグレーションを実行
echo "Running migrations..."
cd /app
alembic upgrade head

# FastAPIアプリケーションを起動
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload