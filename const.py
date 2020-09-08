"""Constants for the autelis integration."""
import logging

_LOGGER = logging.getLogger(__package__)

DOMAIN = "autelis_pool"
AUTELIS_HOST = "host"
AUTELIS_PASSWORD = "password"

AUTELIS_USERNAME = "admin"

AUTELIS_PLATFORMS = ["sensor", "switch", "climate"] # ["binary_sensor", "climate", "sensor", "weather"]


TEMP_SENSORS = {
    "pooltemp": ["Temperature", "Pool"],
    "spatemp": ["Temperature", "Spa"],
    "airtemp": ["Temperature", "Air"],
    "solartemp": ["Temperature", "Solar"],
}

HEAT_SET = {
    "Pool Heat": ["pooltemp", "poolsp", "poolht"],
    "Spa Heat": ["spatemp", "spasp", "spaht"],
}

CIRCUITS = {
    "pump": "Pool",
    "spa": "Spa",
    "aux1": "Spa Extra Jets",
    "aux2": "Sheer Descents",
    "aux3": "Pool Light",
    "aux3": "Spa Light",
    "solarht": "Solar Heating",
}

STATE_SERVICE = "service"
STATE_AUTO = "auto"

MAX_TEMP = 104
MIN_TEMP = 34