#!/bin/bash

download_updated_mac_vendors() {
	local OUT="$1"

	URL="https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"
	if [ -z "$OUT" ]; then
		OUT="$ROOT_DIR/etc/mac-vendor.txt"
	fi

	log "Retrieving $(basename "$OUT")"

	curl --disable --silent "$URL" | sed -e 's/		/	/g' | awk -F'	' '
	BEGIN { OFS="	" }
	NF >= 3 {
	mac=$1; gsub(/:/, "", mac);
	vend=$3; gsub(/ *,.*$/, "", vend);
	print mac, vend
	}' > "$OUT"


	if [[ $? -ne 0 ]]; then
		log "  ERROR during retrieval: $?"
	else
		log "  Retrieval done."
	fi
}
