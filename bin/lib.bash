#!/bin/bash

export _exit_code=0

log() {
	local date=$(date +"%Y/%m/%d %H:%M:%S")
	local script=$(basename "$0")
	local log_file="$(dirname "$0")/../var/shade_$(date +"%Y-%m-%d").log"
	mkdir -p "$(dirname "$log_file")"
	echo "$date $script $*" | tee -a "$log_file"
}

get_config_value() {
	local config="$1"
	local program="$2"
	local default="$3"
	local value=$(jq -r "$program" "$config" 2>/dev/null)

	if [ "$value" == "null" ]; then
		value="$default"
	fi

	echo "$value"
}

require_value() {
	local name="$1"
	local value="$2"
	local valid="$3"

	if [ -z "$value" -o "X$value" == "Xnull" ]; then
		log "ERROR: $name is required."
		_exit_code=$(($_exit_code + 1))
	fi
	if [ -n "$valid" ]; then
		if [[ ! "$value" =~ $valid ]]; then
			log "ERROR: $name is not valid: $value"
			_exit_code=$(($_exit_code + 1))
		fi
	fi
}

exit_if_error() {
	if [ $_exit_code -gt 0 ]; then
		exit $_exit_code
	fi
}

fullpath() {
	local dest="$1"

	if [ -d "$dest" ]; then
		echo "$(cd "$dest"; pwd)"
	elif [ -f "$dest" ]; then
		echo "$(cd $(dirname "$dest"); pwd)"
	else
		echo "$(pwd)/$dest"
	fi
}

ROOT_DIR=$(dirname $(fullpath "$0"))
