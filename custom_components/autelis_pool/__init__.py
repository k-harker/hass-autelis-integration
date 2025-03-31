"""Support for controlling an Autelis pool controller (from www.autelis.com which no longer exists) to control one of several different types of pool control systems"""
import asyncio
from datetime import timedelta
import logging
import time


from homeassistant.const import (
    CONF_PASSWORD,
    CONF_HOST,
    CONF_NAME,
    STATE_ON,
    STATE_OFF
)
from homeassistant.util import Throttle

from .const import (
    DOMAIN, 
    AUTELIS_PLATFORMS, 
    TEMP_SENSORS,
    STATE_AUTO,
    STATE_SERVICE,
    PLATFORMS
)
from .api import AutelisPoolAPI

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Pool Control"
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)


def setup(hass, config):
    """Set up the Autelis component."""
    
    return True

async def async_setup_entry(hass, entry):
    """Set up autelis via a config entry."""
    host = entry.data[CONF_HOST]
    password = entry.data[CONF_PASSWORD]

    data = AutelisData(hass, entry, host=host, password=password)

    await data.update()

    if data.sensors is None:
        _LOGGER.error("Unable to connect to Autelis device")
        return False

    hass.data[DOMAIN] = data


    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
#    for component in AUTELIS_PLATFORMS:
#        hass.async_create_task(
#            hass.config_entries.async_forward_entry_setup(entry, component)
#        )

    return True

async def async_unload_entry(hass, entry):
    """Unload the config entry and platforms."""
    hass.data.pop(DOMAIN)

    tasks = []
    for platform in AUTELIS_PLATFORMS:
        tasks.append(
            hass.config_entries.async_forward_entry_unload(entry, platform)
        )

    return all(await asyncio.gather(*tasks))

class AutelisData:
    """
    Handle getting the latest data from autelis so platforms can use it.
    """

    def __init__(self, hass, entry, host, password):
        """Initialize the Autelis data object."""
        self._hass = hass
        self._entry = entry
        self.host = host
        self.password = password
        self.api = AutelisPoolAPI(hass, f"http://{host}/", password)
        self.sensors = { }
        self.sensors2 = { }
        self.equipment = { }
        self.mode = ""
        self.names = { }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def update(self):
        """Get the latest data from autelis controller"""

        if self.names is None or len(self.names) == 0:
            self.names = await self.api.get_names()
        
        _LOGGER.debug("Updating autelis")
        status = await self.api.get("status.xml")

        temps = status.find("temp")

        if temps is not None:
            for child in temps:
                value = child.text
                self.sensors[child.tag] = value
        else:
            _LOGGER.error("temps is None")
            
        equip = status.find("equipment")

        if equip is not None:
            for child in equip:
                value = child.text
                self.equipment[child.tag] = value
        else:
            _LOGGER.error("equip is None")
        
        #vbat = status.find(".//vbat")
        
        #if vbat is not None:
        #    self.sensors2["vbat"] = vbat * 0.01464
        #else:
        #    _LOGGER.debug("vbat does not have a value")
        
        #lowbat = status.find(".//lowbat")
        
        #if lowbat is not None:
        #    self.sensors2["lowbat"] = lowbat == "1"
        #else:
        #    _LOGGER.debug("lowbat does not have a value")
        
        opmode = status.find(".//opmode")
        # freeze = status.find("freeze")

        if opmode is not None:
            self.mode = STATE_AUTO if opmode.text == "0" else STATE_SERVICE
        else:
            self.mode = STATE_SERVICE
            _LOGGER.error("opmode is None")

        # self.freeze = STATE_ON if freeze && freeze.text == "1" else STATE_OFF
        return
