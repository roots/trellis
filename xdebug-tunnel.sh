#!/usr/bin/env bash
# Usage:
#   To open a tunnel: ./xdebug-tunnel.sh example_com_prod
#   To close a tunnel: ./xdebug-tunnel.sh example_com_prod close

SSH_HOST="-e xdebug_tunnel_inventory_host=$1"
XDEBUG_ENABLE="-e xdebug_remote_enable=$([[ $2 == "close" ]] && echo 0 || echo 1)"

if [[ -n $DEBUG ]]; then
  PARAMS="$PARAMS ${VERBOSITY:--vvvv}"
fi

ansible-playbook xdebug-tunnel.yml $SSH_HOST $XDEBUG_ENABLE $PARAMS
