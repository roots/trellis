#!/usr/bin/env bash
# Usage:
#   To open a tunnel: bin/xdebug-tunnel.sh production example_com_prod
#   To close a tunnel: bin/xdebug-tunnel.sh production example_com_prod close

ENV="-e env=${1}"
SSH_HOST="-e xdebug_tunnel_ssh_host=${2}"
MAYBE_CLOSE="${3}"
CLOSE_CONNECTION=

if [[ "${MAYBE_CLOSE}" == 'close' ]]; then
  CLOSE_CONNECTION="-e xdebug_tunnel_close=true"
fi

ansible-playbook xdebug-tunnel.yml ${ENV} ${SSH_HOST} ${CLOSE_CONNECTION}
