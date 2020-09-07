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
        dev.append(HeaterTemp(data, item, item[0], item[1], item[2]))

    async_add_entities(dev, True)


class HeaterTemp(ClimateDevice):
    """Representation of an Autelis pool control."""

    def __init__(
        self,
        data,
        friendly_name,
        sensor_name,
        target_name,
        equip_name,
        icon=None,
    ):
        """Initialize a new Autelis sensor."""
        self.data = data
        self.friendly_name = friendly_name
        self.sensor_name = sensor_name
        self.target_name = target_name
        self.equip_name = equip_name
        self.target_temp = None
        self.current_temp = None
        self._unit_of_measurement = TEMP_FAHRENHEIT
        self._icon = icon
        _LOGGER.debug("Created Autelis sensor %r", self)

    @property
    def unique_id(self):
        """Return a unique identifier for this ecobee thermostat."""
        return self.sensor_name


    @property
    def name(self):
        """Return the name of the sensor."""
        return self.friendly_name

    @property
    def state(self):
        """Return the state of the sensor."""
        sensor_unit = self.unit_of_measurement
        if sensor_unit in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
            # API sometimes returns null and not 0
            if self.current_temp is None:
                self.current_temp = 0
            return round(self.current_temp, 2)
        return self.current_temp

    async def async_set_hvac_mode(self, hvac_mode):
        self.mode = hvac_mode
        newMode = 1 if hvac_mode == HVAC_MODE_HEAT else 0
        self.data.api.control(self.equip_name, newMode)

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temp = kwargs.get(ATTR_TEMPERATURE)

        if temp > 104:
            temp = 104

        self.target_temp = temp
        self.data.api.control(self.target_name, temp)

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
        return self.current_temp

    @property
    def target_temperature(self):
        return self.target_temp

    @property
    def hvac_action(self):
        """Return current HVAC action."""
        heatMode = self.data.equipment[self.equip_name]

        if heatMode == "1"
            return CURRENT_HVAC_IDLE

        if heatMode == "2":
            return CURRENT_HVAC_HEAT

        return CURRENT_HVAC_OFF

    async def async_update(self):
        """Get the latest state of the sensor."""
        await self.data.update()

        self.current_temp = self.data.sensors[self.sensor_name]
        self.target_temp = self.data.sensors[self.target_name]
        heatMode = self.data.equipment[self.equip_name]
        self.mode = HVAC_MODE_HEAT if heatMode > 0 else HVAC_MODE_OFF

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return self._icon