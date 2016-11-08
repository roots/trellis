#!/usr/bin/env bash

show_usage() {
  echo "
Usage: bin/xdebug-tunnel.sh <action> <host>

<action> can be 'open' or 'close'
<host> is the hostname, IP, or inventory alias in your \`hosts/<environment>\` file.

Examples:
  To open a tunnel:
    bin/xdebug-tunnel.sh open 12.34.56.78

  To close a tunnel:
    bin/xdebug-tunnel.sh close 12.34.56.78
"
}

if [[ $1 == "open" ]]; then
  REMOTE_ENABLE=1
elif [[ $1 == "close" ]]; then
  REMOTE_ENABLE=0
else
  >&2 echo "The provided <action> argument '${1}' is not acceptable."
  show_usage
  exit 1
fi

if [[ -z $2 ]]; then
  >&2 echo "The <host> argument is required."
  show_usage
  exit 1
fi

XDEBUG_ENABLE="-e xdebug_remote_enable=${REMOTE_ENABLE}"
SSH_HOST="-e xdebug_tunnel_inventory_host=$2"

if [[ -n $DEBUG ]]; then
  PARAMS="$PARAMS ${VERBOSITY:--vvvv}"
fi

ansible-playbook xdebug-tunnel.yml $XDEBUG_ENABLE $SSH_HOST $PARAMS
