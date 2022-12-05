# Apphoy WebApp
Sailing organiser's web application.

## Setup and Execution

1. Start application with Docker Compose:
```shell
docker-compose up -d
```
2. Create superuser with the command:
```shell
./manage_in_docker.sh createsuperuser
```
3. Go to the main page of the application: http://127.0.0.1:8000/persons/
4. Login using the credentials for the created superuser.