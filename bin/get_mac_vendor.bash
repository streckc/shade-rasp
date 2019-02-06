#!/bin/bash

. "$(dirname "$0")/lib.bash"

URL="https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"
OUT="$ROOT_DIR/etc/mac-vendor.txt"

log "Retrieving $(basename "$OUT")"

curl "$URL" | sed -e 's/		/	/g' | awk -F'	' '
BEGIN { OFS="	" }
NF >= 3 {
mac=$1; gsub(/:/, "", mac);
vend=$3; gsub(/ *,.*$/, "", vend);
print mac, vend
}' > "$OUT"


if [[ $? -ne 0 ]]; then
	log "ERROR during retrieval: $?"
else
	log "Retrieval done."
fi
