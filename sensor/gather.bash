
sudo arp-scan --retry=8 --ignoredups -I wlan0 --localnet -macfile=mac-vendor.txt

avahi-browse --all --parsable --terminate --verbose --resolve
