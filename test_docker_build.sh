#docker-compose down
docker stop data-pipelines-container
docker rm container data-pipelines-container

docker build -t data-pipelines-reference-app:latest .
docker run -id  --env-file ../.env --name data-pipelines-container data-pipelines-reference-app:latest

docker exec -it data-pipelines-container bash