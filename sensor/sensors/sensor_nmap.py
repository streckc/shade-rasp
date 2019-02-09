
from .reporting import sensor_report

_name = 'nmap-sensor'

def nmap_sensor(config):
    global _name

    result = sensor_report(_name)

    return result

