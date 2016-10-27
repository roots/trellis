#!/usr/bin/env bash
# Usage:
#   To open a tunnel: bin/xdebug-tunnel.sh example_com_prod
#   To close a tunnel: bin/xdebug-tunnel.sh example_com_prod close

SSH_HOST="-e xdebug_tunnel_ssh_host=${1}"
MAYBE_CLOSE="${2}"
CLOSE_CONNECTION=

if [[ "${MAYBE_CLOSE}" == 'close' ]]; then
  CLOSE_CONNECTION="-e xdebug_tunnel_close=true"
fi

ansible-playbook xdebug-tunnel.yml ${SSH_HOST} ${CLOSE_CONNECTION}
