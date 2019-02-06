#!/bin/bash

WD=$(dirname "$0")

sudo arp-scan --retry=8 --ignoredups -I wlan0 --localnet -macfile="$WD/mac-vendor.txt"
