# """Support for controlling Heaters through Autelis."""
import logging

import requests

from homeassistant.const import TEMP_CELSIUS, TEMP_FAHRENHEIT
from homeassistant.helpers.entity import Entity
from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import (
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_TEMPERATURE_RANGE,
)
from .const import DOMAIN, HEAT_SET

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up autelis heater temps."""
    data = hass.data[DOMAIN]
    dev = []
    for item in HEAT_SET.items():
        dev.append(HeaterTemp(data, item[0]))

    async_add_entities(dev, True)


class HeaterTemp(ClimateDevice):
    """Representation of an Autelis pool control."""

    def __init__(
        self,
        data,
        sensor_name,
        icon=None,
    ):
        """Initialize a new Autelis sensor."""
        self.data = data        
        self.sensor_name = sensor_name
        self._name = f"{sensor_name} "
        self.api = api
        self._state = None
        self._unit_of_measurement = TEMP_FAHRENHEIT
        self._icon = icon
        _LOGGER.debug("Created Autelis sensor %r", self)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        sensor_unit = self.unit_of_measurement
        if sensor_unit in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
            # API sometimes returns null and not 0
            if self._state is None:
                self._state = 0
            return round(self._state, 2)
        return self._state

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""

    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def hvac_modes(self):
        return HVAC_MODE_OFF, HVAC_MODE_HEAT

    @property
    def temperature_unit(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def current_temperature(self):
        return 80

    @property
    def target_temperature(self):
        return 100

    @property
    def target_temperature_high(self):
        return 104

    @property
    def target_temperature_low(self):
        return 104

    async def async_update(self):
        """Get the latest state of the sensor."""
        await self.data.update()

        self._state = self.data.sensors[self.sensor_name]

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return self._icon