
from copy import deepcopy

from .util import deep_merge

_config = {}


def get_config(config={}):
    global _config
    return deepcopy(_config)


def set_config(config={}):
    global _config
    _config = deepcopy(config)


def update_config(config={}):
    global _config
    _config = deep_merge(_config, config)


def get_config_value(name, default=None):
    global _config

    value = _config
    for key in name.split('.'):
        if key in value:
            value = value[key]
        else:
            return default

    return value

