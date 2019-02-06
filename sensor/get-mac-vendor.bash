#!/bin/bash

URL="https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"
OUT="mac-vendor.txt"

curl "$URL" | sed -e 's/		/	/g' | awk -F'	' '
BEGIN { OFS="	" }
NF >= 3 {
mac=$1; gsub(/:/, "", mac);
vend=$3; gsub(/ *,.*$/, "", vend);
print mac, vend
}' | tee "$OUT"
