name = 'sensors'

from .sensor_arp_scan import arp_scan_sensor
from .sensor_avahi_browse import avahi_browse_sensor
from .sensor_nmap import nmap_sensor
from .sensor_vmstat import vmstat_sensor
from .sensor_vmstat import df_sensor

sensor_list = {
    'arp-scan': arp_scan_sensor,
    'avahi-browse': avahi_browse_sensor,
    'nmap': nmap_sensor,
    'vmstat': vmstat_sensor,
    'df': df_sensor
}

