name = 'sensors'

from .sensor_arp_scan import arp_scan_sensor
#from .sensor_avahi_browse import avahi_browse_sensor
from .sensor_nmap import nmap_sensor

sensor_list = {
    'arp-scan': arp_scan_sensor,
    'nmap': nmap_sensor
}
#    'avahi-browse': avahi_browse_sensor,

