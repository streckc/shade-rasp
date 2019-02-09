
from .reporting import sensor_report

_name = 'avahi-browse-sensor'

def avahi_browse_sensor(config):
    global _name

    result = sensor_report(_name)

    return result

