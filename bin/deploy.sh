#!/bin/bash
shopt -s nullglob

DEPLOY_CMD="ansible-playbook deploy.yml -e env=$1 -e site=$2"
ENVIRONMENTS=( hosts/* )
ENVIRONMENTS=( "${ENVIRONMENTS[@]##*/}" )
NUM_ARGS=2
BRANCH_NAME="$(git symbolic-ref HEAD 2>/dev/null)" ||
BRANCH_NAME="(unnamed branch)"     # detached HEAD
BRANCH_NAME=${BRANCH_NAME##refs/heads/}

show_usage() {
  echo "Usage: deploy <environment> <site name>

<environment> is the environment to deploy to ("staging", "production", etc)
<site name> is the WordPress site to deploy (name defined in "wordpress_sites")

Available environments:
`( IFS=$'\n'; echo "${ENVIRONMENTS[*]}" )`

Examples:
  deploy staging example.com
  deploy production example.com
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

if [[ $BRANCH_NAME != 'master' ]]
then
  echo -e 'You are not on master branch. Are you sure you want to continue? [y/N]'
  read -r RESPONSE
fi
if [[ $RESPONSE =~ ^([yY][eE][sS]|[yY])$ ]]
  then
    $DEPLOY_CMD
  else
    echo -e 'Aborted'
    exit 0
fi
