#!/usr/bin/env bash
# Usage:
#   To open a tunnel: bin/xdebug-tunnel.sh example_com_prod
#   To close a tunnel: bin/xdebug-tunnel.sh example_com_prod close

SSH_HOST="-e xdebug_tunnel_inventory_host=${1}"
MAYBE_CLOSE="${2}"
CLOSE_CONNECTION=
DEBUG="${DEBUG:-}"
VERBOSITY="${VERBOSITY:--vvvv}"
PARAMs="${PARAMS:-}"

if [[ "${MAYBE_CLOSE}" == 'close' ]]; then
  PARAMS="${PARAMS} -e xdebug_tunnel_close=true -e xdebug_install=false"
else
  PARAMS="${PARAMS} -e xdebug_install=true"
fi

if [[ -n "${DEBUG}" ]]; then
  PARAMS="${PARAMS} ${VERBOSITY}"
fi

PARAMS="${SSH_HOST} ${CLOSE_CONNECTION} ${PARAMS}"
ansible-playbook xdebug-tunnel.yml ${PARAMS}
