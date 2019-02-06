#!/bin/bash

. "$(dirname "$0")/lib.bash"

main() {
	log "Start."
	setup_directories
	check_requirements
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
		log "Securing keys directory..."
		chmod 700 "$ROOT_DIR/etc/keys"
	fi

	exit_if_error
}

check_requirements() {
	log "Checking directories..."

	SHELL_REQS=$(ls -d "$ROOT_DIR/etc/shell_reqs.txt")
	require_value "$ROOT_DIR/etc/shell_reqs.txt" "$SHELL_REQS"

	if [ -n "$SHELL_REQS" ]; then
		cat "$SHELL_REQS" | while read REQ; do
			log "Checking for $REQ..."
			require_value "$REQ" "$REQ"
		done
	fi
	exit_if_error
}

main
