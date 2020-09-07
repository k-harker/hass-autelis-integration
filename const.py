"""Constants for the autelis integration."""
import logging

_LOGGER = logging.getLogger(__package__)

DOMAIN = "autelis_pool"
AUTELIS_HOST = "host"
AUTELIS_PASSWORD = "password"

AUTELIS_USERNAME = "admin"

AUTELIS_PLATFORMS = ["sensor", "switch"] # ["binary_sensor", "climate", "sensor", "weather"]


TEMP_SENSORS = {
    "pooltemp": ["Temperature", "Pool"],
    "spatemp": ["Temperature", "Spa"],
    "airtemp": ["Temperature", "Air"],
    "solartemp": ["Temperature", "Solar"],
}

HEAT_SET = {
    "poolsp": ["Pool Heat", "pooltemp", "poolht"],
    "spasp": ["Spa Heat", "spatemp", "spaht"],
}

CIRCUITS = {
    "pump": "Pool",
    "spa": "Spa",
    "aux1": "Spa Extra Jets",
    "aux2": "Sheer Descents",
    "aux3": "Pool Light",
    "aux3": "Spa Light",
}

STATE_SERVICE = "service"
STATE_AUTO = "auto"