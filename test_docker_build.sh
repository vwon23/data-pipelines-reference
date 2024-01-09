## Script used for building docker images and running container
docker stop data-pipeline-container
docker rm data-pipeline-container

docker build -t data-pipelines-reference-app:latest .
docker run -id  --env-file ../.env --name data-pipeline-container data-pipelines-reference-app:latest

docker exec -it data-pipeline-container bash