#!/bin/sh

# set -e

# HOST="$1"
# echo $HOST
# shift
# cmd="$@"

# until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$HOST" -U "postgres" -c '\q'; do
#   >&2 echo "Postgres is unavailable - sleeping"
#   sleep 1
# done

# >&2 echo "Postgres is up - executing command"
# exec $cmd

flask db upgrade

exec gunicorn -w 4 -b :8000 app:app