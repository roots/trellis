#!/bin/bash
shopt -s nullglob

DATABASE_PULL_CMD="ansible-playbook database-pull.yml -e env=$1 -e site=$2"
DATABASE_PUSH_CMD="ansible-playbook database-push.yml -e env=$1 -e site=$2"
DATABASE_BACKUP_CMD="ansible-playbook database-backup.yml -e env=$1 -e site=$2"
ENVIRONMENTS=( hosts/* )
ENVIRONMENTS=( "${ENVIRONMENTS[@]##*/}" )
NUM_ARGS=3

show_usage() {
  echo "Usage: ./database.sh <environment> <site name> <mode>

<environment> is the environment to sync database ("staging", "production", etc)
<site name> is the WordPress site to sync database (name defined in "wordpress_sites")
<mode> is the sync mode ("push", "pull", "backup")

Available environments:
`( IFS=$'\n'; echo "${ENVIRONMENTS[*]}" )`

Examples:
  ./bin/database.sh staging example.com push
  ./bin/database.sh staging example.com pull
  ./bin/database.sh staging example.com backup
  ./bin/database.sh production example.com push
  ./bin/database.sh production example.com pull
  ./bin/database.sh production example.com backup
"
}

HOSTS_FILE="hosts/$1"

[[ $# -ne $NUM_ARGS || $1 = -h ]] && { show_usage; exit 0; }

if [[ ! -e $HOSTS_FILE ]]; then
  echo "Error: $1 is not a valid environment ($HOSTS_FILE does not exist)."
  echo
  echo "Available environments:"
  ( IFS=$'\n'; echo "${ENVIRONMENTS[*]}" )
  exit 0
fi

case $3 in
  push)
    $DATABASE_PUSH_CMD
  ;;
  pull)
    $DATABASE_PULL_CMD
  ;;
  backup)
    $DATABASE_BACKUP_CMD
  ;;
  *)
    show_usage
  ;;
esac
