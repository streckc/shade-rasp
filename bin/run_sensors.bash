#!/bin/bash

. "$(dirname "$0")/lib.bash"

ACTION="$1"

SCRIPT="run_sensors.py"
CONF=$(ls -d "$ROOT_DIR/etc/config.json" 2>/dev/null)
SENSORS=$(ls -d "$ROOT_DIR/sensor/$SCRIPT" 2>/dev/null)
API=$(get_config_value "$CONF" ".api.port" "8088")

main() {
	local action="$1"

	verify_config

	case "$action" in
		"start")
			start_sensors
			;;
		"stop")
			stop_sensors
			;;
		"check")
			check_tunnel
			;;
		"restart")
			stop_sensors
			sleep 1
			start_sensors
			;;
		"status")
			sensors_status
			;;
		*)
			echo "Usage: $(basename "$0") <start|stop|check|status>"
			;;
	esac
}

verify_config() {
	require_value "Config" "$CONF"
	require_value "Sensor Binary" "$SENSORS"
	require_value "API" "$API"
	exit_if_error
}

start_sensors() {
	local PID=""

	log "Starting sensors."
	nohup $SENSORS \
		--log "$ROOT_DIR/logs/shade___DATE__.log" \
		--config "$ROOT_DIR/etc/config.json" \
		>/dev/null 2>>"$ROOT_DIR/logs/error.log" &

	sleep 1

	PID=$(get_sensors_pid)
	if [ -n "$PID" ]; then
		log "Sensors started. ($PID)"
	else
		log "An error occurred starting sensors: $?."
	fi
}

stop_sensors() {
	log "Stopping sensors."
	local PID=$(get_sensors_pid)

	if [ -n "$PID" ]; then
		kill $PID
		log "Sensors stopped. ($PID)"
	else
		log "No sensors found to stop."
	fi
}

check_tunnel() {
	local PID=$(get_sensors_pid)
	if [ -z "$PID" ]; then
		start_sensors
	fi
}

sensors_status() {
	local PID=$(get_sensors_pid)
	if [ -n "$PID" ]; then
		log "Running PID: $PID"
	else
		log "Sensors are not running."
	fi
}

get_sensors_pid() {
	ps aux | egrep "python3.*$SCRIPT" | grep -v grep | awk '{ print $2 }'
}

main "$ACTION"
