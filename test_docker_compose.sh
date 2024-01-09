## Script running container using docker-compose.yml file.
docker-compose down
docker-compose --env-file ../.env up --build -d
docker exec -it data-pipeline-container bash