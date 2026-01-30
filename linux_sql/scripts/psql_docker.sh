#!/bin/sh

# -----------------------------------------
# psql_docker.sh
# Postgres Docker container: jrvs-psql
#
# Usage:
#   ./scripts/psql_docker.sh create <db_username> <db_password>
# -----------------------------------------

cmd=$1
db_username=$2
db_password=$3

container_name="jrvs-psql"
volume_name="pgdata"
image="postgres:9.6-alpine"

# Start docker engine if not running
sudo systemctl status docker >/dev/null 2>&1 || sudo systemctl start docker

# Check whether container exists
docker container inspect "$container_name" >/dev/null 2>&1
container_exists=$?   # 0 = exists, non-zero = doesn't exist

case "$cmd" in
  create)
    # Require username + password
    if [ $# -ne 3 ]; then
      echo "ERROR: create requires db_username and db_password"
      echo "Usage: ./scripts/psql_docker.sh create <db_username> <db_password>"
      exit 1
    fi

    # If container already exists, error out
    if [ $container_exists -eq 0 ]; then
      echo "ERROR: Container '$container_name' already exists"
      exit 1
    fi

    # Create volume if not exists (idempotent)
    docker volume create "$volume_name" >/dev/null

    # Create and start container
    # Note: default Postgres user in the image is 'postgres'
    docker run --name "$container_name" \
      -e POSTGRES_PASSWORD="$db_password" \
      -d \
      -v "$volume_name":/var/lib/postgresql/data \
      -p 5432:5432 \
      "$image"

    exit $?
    ;;

  start|stop)
    # Container must exist
    if [ $container_exists -ne 0 ]; then
      echo "ERROR: Container '$container_name' does not exist. Run create first."
      exit 1
    fi

    docker container "$cmd" "$container_name"
    exit $?
    ;;

  *)
    echo "ERROR: Illegal command"
    echo "Commands: create|start|stop"
    echo "Usage:"
    echo "  ./scripts/psql_docker.sh create <db_username> <db_password>"
    echo "  ./scripts/psql_docker.sh start"
    echo "  ./scripts/psql_docker.sh stop"
    exit 1
    ;;
esac

