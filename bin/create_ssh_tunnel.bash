#!/bin/bash

. "$(dirname "$0")/lib.bash"

CONF=$(ls -d "$ROOT_DIR/etc/config.json" 2>/dev/null)
SSH=$(which ssh)
PIDOF=$(which pidof)
require_value "Config" "$CONF"
require_value "SSH Binary" "$SSH"
require_value "PIDOF Binary" "$PIDOF"
exit_if_error

USER=$(get_config_value "$CONF" ".reverse.user")
KEY=$(get_config_value "$CONF" ".reverse.key")
SERVER=$(get_config_value "$CONF" ".reverse.host")
PORT=$(get_config_value "$CONF" ".reverse.port" "22")
LISTEN=$(get_config_value "$CONF" ".reverse.listen" "2222")
API=$(get_config_value "$CONF" ".api.port" "8088")

require_value "User" "$USER"
require_value "Server" "$SERVER"
require_value "Port" "$PORT"
require_value "Key" "$KEY"
require_value "Listen" "$LISTEN"
require_value "API" "$API"
exit_if_error

#log "Listen on $LISTEN at $USER@$SERVER:$PORT ($KEY)"

create_tunnel() {
	$SSH -N \
	       	-o PasswordAuthentication=no \
	       	-o ServerAliveInterval=180 \
	       	-o ServerAliveCountMax=5 \
	       	-R $LISTEN:127.0.0.1:$PORT \
	       	-L $API:127.0.0.1:$API \
	       	-i "$ROOT_DIR/etc/keys/$KEY" \
	       	$USER@$SERVER
	
	if [[ $? -eq 0 ]]; then
		log "Tunnel created."
	else
		log "An error occurred creating tunnel: $?."
	fi
}

$PIDOF ssh
if [[ $? -ne 0 ]]; then
	log "Creating tunnel."
	create_tunnel
	log "Tunnel done."
fi
