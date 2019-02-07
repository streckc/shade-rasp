#!/bin/bash

. "$(dirname "$0")/lib.bash"

main() {
	log "Start."
	setup_directories
	check_requirements
	check_config
	create_crontab
	exit_if_error
	log "Done."
}

setup_directories() {
	log "Making directories..."

	for DIR in logs var etc/keys; do
		if [ ! -d "$ROOT_DIR/$DIR" ]; then
			log "  ... $ROOT_DIR/$DIR"
			mkdir -p "$ROOT_DIR/$DIR"
		else
			log "  ... $ROOT_DIR/$DIR exists"
		fi
		require_value "$DIR" "$(ls -d "$ROOT_DIR/$DIR")"
	done

	if [ -d "$ROOT_DIR/etc/keys" ]; then
		log "  Securing keys directory..."
		chmod 700 "$ROOT_DIR/etc/keys"
	fi
}

check_requirements() {
	log "Checking directories..."

	SHELL_REQS=$(ls -d "$ROOT_DIR/etc/shell_reqs.txt")
	require_value "$ROOT_DIR/etc/shell_reqs.txt" "$SHELL_REQS"

	if [ -n "$SHELL_REQS" ]; then
		cat "$SHELL_REQS" | while read REQ; do
			log "  Checking for $REQ..."
			require_value "$REQ" "$(which "$REQ")"
		done
	fi
}

check_config() {
	log "Checking config..."

	local CONF="$ROOT_DIR/etc/config.json"

	log "  ... location"
	require_value "$ROOT_DIR/etc/config.json" "$(ls -d "$CONF" 2>/dev/null)"

	log "  ... valid json"
	require_value "jq compiles" "$(jq "." "$ROOT_DIR/etc/config.json" 2>/dev/null)"

	log "  ... values"
	require_value "reverse.user" "$(get_config_value "$CONF" ".reverse.user")"
	require_value "reverse.host" "$(get_config_value "$CONF" ".reverse.host")"
	require_value "reverse.key" "$(get_config_value "$CONF" ".reverse.key")"

}

create_crontab() {
	log "Creating crontab..."
	local TEMPLATE="$ROOT_DIR/etc/crontab.template"
	local CRONTAB="$ROOT_DIR/crontab"

	if [ -f "$CRONTAB" ]; then
		log "  Crontab exists, not replacing: $CRONTAB"
	elif [ ! -f "$TEMPLATE" ]; then
		log "  Template missing, not creating: $TEMPLATE"
	else
		cat "$TEMPLATE" | sed -e "s#__DIR__#$ROOT_DIR#g" > $CRONTAB
		log "  Crontab created: $CRONTAB"
	fi
}

main

