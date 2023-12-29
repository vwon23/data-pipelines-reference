# data-pipelines-reference
Codes used for learning materials on O Reilly's "Data Pipeline Pocket Reference" by James Densmore.

### Getting Started
Create .env file in parent folder of this repository for sensitive environment variables such as passwords.
In addition, user need to configure credentials to login to AWS run locally. (login profile and role used to connect to AWS is defined in docker-compose.override.yml)

#### Example of .env content:
env=dev
aws_rgn=us-west-2
mysql_username=admin
mysql_password=xyz
snowflake_username=admin
snowflake_password=xyz

## Run docker container locally
1. Setup .env in parent folder of repo
2. Run command "docker-compose --env-file ../.env up --build -d" to build and run docker container
3. Run command "docker exec -it {name_of_container} bash to test scripts inside container
4. Run command "docker-compose down" when done testing to remove docker containers

### Reference for docker-compose.yml used
Added docker-compose.yml and docker-compose.override.ymml to get IAM Role permission from AWS when running container locally.
Please visit https://aws.amazon.com/blogs/compute/a-guide-to-locally-testing-containers-with-amazon-ecs-local-endpoints-and-docker-compose/ for more details.