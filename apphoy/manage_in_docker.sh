# run manage.py command in `web` container
# usage example: `./manage_in_docker.sh shell_plus`
docker-compose run --rm apphoy_web python manage.py ${@}