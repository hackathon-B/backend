#!/bin/bash

#Docker Composeで定義されたすべてのサービスを停止し、削除
docker compose -f "docker-compose.yml"down
#未使用のDockerイメージを削除
docker image prune -f
#停止したすべてのDockerコンテナを削除
docker container prune -f
#未使用のDockerボリュームを削除
docker volume prune -f
#未使用のDockerネットワークを削除
docker network prune -f