#!/bin/bash
shopt -s nullglob

UPLOADS_CMD="ansible-playbook uploads.yml -e env=$1 -e site=$2 -e mode=$3"
ENVIRONMENTS=( hosts/* )
ENVIRONMENTS=( "${ENVIRONMENTS[@]##*/}" )
NUM_ARGS=3

show_usage() {
  echo "Usage: ./uploads.sh <environment> <site name> <mode>

<environment> is the environment to sync uploads ("staging", "production", etc)
<site name> is the WordPress site to sync uploads (name defined in "wordpress_sites")
<mode> is the sync mode ("push", "pull")

Available environments:
`( IFS=$'\n'; echo "${ENVIRONMENTS[*]}" )`

Examples:
  ./bin/uploads.sh staging example.com push
  ./bin/uploads.sh staging example.com pull
  ./bin/uploads.sh production example.com push
  ./bin/uploads.sh production example.com pull
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

echo -e -n "Are you sure? (Y/n) "
read -n 1 answer
echo " "
if [ "$answer" == "Y" ]; then
  $UPLOADS_CMD
else
  echo "Operation aborted."
fi
