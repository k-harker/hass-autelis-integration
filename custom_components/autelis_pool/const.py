"""Constants for the autelis integration."""
import logging
from homeassistant.const import Platform

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
    "soltemp": ["Temperature", "Solar"],
}

HEAT_SET = {
    "Pool Heat": ["pooltemp", "poolsp", "poolht"],
    "Spa Heat": ["spatemp", "spasp", "spaht"],
}

CIRCUITS = {
    # "pump": "Pool",
    # "spa": "Spa",
    # "solarht": "Solar Heating",
    # "cleaner": "Cleaner",
}

PLATFORMS = [
    Platform.CLIMATE,
    Platform.SENSOR,
    Platform.SWITCH,
]

STATE_SERVICE = "service"
STATE_AUTO = "auto"

MAX_TEMP = 104
MIN_TEMP = 34

# these constants represent which type of autelis device
# we are talking to
AUTELIS_JANDY = 0    #jandy aqualink version
AUTELIS_PENTAIR = 1  #pentair intellitouch version
