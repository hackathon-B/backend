# Dockerfile

FROM tiangolo/uvicorn-gunicorn:python3.11

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

WORKDIR /app

# netcatをインストール（データベース待機用）
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# プロジェクト全体をコピー 
COPY . .

# entrypoint.shに実行権限を付与
RUN chmod +x /app/docker/app/entrypoint.sh

ENV PYTHONPATH=/app