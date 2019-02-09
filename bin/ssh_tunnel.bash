#!/bin/bash

. "$(dirname "$0")/lib.bash"

ACTION="$1"

CONF=$(ls -d "$ROOT_DIR/etc/config.json" 2>/dev/null)
SSH=$(which ssh)
USER=$(get_config_value "$CONF" ".reverse.user")
KEY=$(get_config_value "$CONF" ".reverse.key")
SERVER=$(get_config_value "$CONF" ".reverse.host")
PORT=$(get_config_value "$CONF" ".reverse.port" "22")
LISTEN=$(get_config_value "$CONF" ".reverse.listen" "2222")
API=$(get_config_value "$CONF" ".api.port" "8088")

main() {
	local action="$1"

	verify_config

	case "$action" in
		"start")
			create_tunnel
			;;
		"stop")
			destroy_tunnel
			;;
		"check")
			check_tunnel
			;;
		"restart")
			destroy_tunnel
			create_tunnel
			;;
		"status")
			tunnel_status
			;;
		*)
			echo "Usage: $(basename "$0") <start|stop|check|status>"
			;;
	esac
}

verify_config() {
	require_value "Config" "$CONF"
	require_value "SSH Binary" "$SSH"

	require_value "User" "$USER"
	require_value "Server" "$SERVER"
	require_value "Port" "$PORT"
	require_value "Key" "$KEY"
	require_value "Listen" "$LISTEN"
	require_value "API" "$API"
	exit_if_error
}

create_tunnel() {
	local PID=""

	log "Creating tunnel."
	$SSH -Nf \
	       	-o PasswordAuthentication=no \
	       	-o ServerAliveInterval=180 \
	       	-o ServerAliveCountMax=5 \
	       	-R $LISTEN:127.0.0.1:$PORT \
	       	-L $API:127.0.0.1:$API \
	       	-i "$ROOT_DIR/etc/keys/$KEY" \
	       	$USER@$SERVER
	
	sleep 1

	PID=$(get_ssh_pid)
	if [ -n "$PID" ]; then
		log "Tunnel created. ($PID)"
	else
		log "An error occurred creating tunnel: $?."
	fi
}

destroy_tunnel() {
	log "Destroying tunnel."
	local PID=$(get_ssh_pid)

	if [ -n "$PID" ]; then
		kill $PID
		log "Tunnel destroyed. ($PID)"
	else
		log "No tunnel found to destroy."
	fi
}

check_tunnel() {
	local PID=$(get_ssh_pid)
	if [ -z "$PID" ]; then
		create_tunnel
	fi
}

tunnel_status() {
	local PID=$(get_ssh_pid)
	if [ -n "$PID" ]; then
		log "Running PID: $PID"
		curl http://127.0.0.1:$API >/dev/null 2>&1
		if [ $? -gt 0 ]; then
			log "API is NOT available."
		else
			log "API is available."
		fi
	else
		log "Tunnel not running."
	fi
}

get_ssh_pid() {
	ps aux | egrep "ssh.*$USER@$SERVER" | grep -v grep | awk '{ print $2 }'
}

main "$ACTION"
