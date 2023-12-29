docker-compose down
docker-compose --env-file ../.env up --build -d
docker exec -it data-pipelines-container bash