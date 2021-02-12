# """Support for controlling Heaters through Autelis."""
import logging
import collections

import requests

from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS, TEMP_FAHRENHEIT
from homeassistant.helpers.entity import Entity
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    CURRENT_HVAC_OFF,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_TEMPERATURE_RANGE,
)
from .const import DOMAIN, HEAT_SET, _LOGGER, MAX_TEMP, MIN_TEMP

AUTELIS_HEAT_TO_ACTION = collections.OrderedDict(
    [
        (0, CURRENT_HVAC_OFF),
        (1, CURRENT_HVAC_IDLE),
        (2, CURRENT_HVAC_HEAT),
    ]
)

AUTELIS_HEAT_TO_MODE = collections.OrderedDict(
    [
        (0, HVAC_MODE_OFF),
        (1, HVAC_MODE_HEAT),
        (2, HVAC_MODE_HEAT),
    ]
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up autelis heater temps."""
    data = hass.data[DOMAIN]
    dev = []
    for item in HEAT_SET.items():
        dev.append(HeaterTemp(data, item[0], item[1][0], item[1][1], item[1][2]))

    async_add_entities(dev, True)


class HeaterTemp(ClimateEntity):
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
        self.mode = None
        self.action = None
        _LOGGER.debug("Created Autelis sensor %r", self)

    @property
    def unique_id(self):
        """Return a unique identifier for this ecobee thermostat."""
        return self.sensor_name

    @property
    def available(self):
        """Return if the switch is available to be turned on."""
        return int(self.data.equipment.runstate) > 7 and
            self.data.equipment.opmode == "0"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.friendly_name

    async def async_set_hvac_mode(self, hvac_mode):
        # _LOGGER.warn(f"Set Mode {hvac_mode} {self.mode}")
        self.mode = hvac_mode
        newMode = 1 if hvac_mode == HVAC_MODE_HEAT else 0
        self.data.equipment[self.equip_name] = newMode
        await self.data.api.control(self.equip_name, newMode)

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temp = kwargs.get(ATTR_TEMPERATURE)

        if temp > 104:
            temp = 104

        tempInt = int(temp)
        self.target_temp = tempInt
        self.data.sensors[self.target_name] = str(tempInt)
        await self.data.api.control(self.target_name, tempInt, "temp")

        # _LOGGER.warn(f"Setting temp to {tempInt}")

    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def hvac_modes(self):
        return HVAC_MODE_OFF, HVAC_MODE_HEAT

    @property
    def hvac_mode(self):
        """Return current operation."""
        return self.mode

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
    def target_temperature_high(self):
        return MAX_TEMP

    @property
    def target_temperature_low(self):
        return MIN_TEMP

    @property
    def max_temp(self):
        return MAX_TEMP

    @property
    def min_temp(self):
        return MIN_TEMP


    @property
    def hvac_action(self):
        """Return current HVAC action."""
        return self.action

    async def async_update(self):
        """Get the latest state of the sensor."""
        await self.data.update()

        self.current_temp = int(self.data.sensors[self.sensor_name])
        self.target_temp = int(self.data.sensors[self.target_name])
        heatMode = int(self.data.equipment[self.equip_name])

        self.mode = AUTELIS_HEAT_TO_MODE[heatMode]
        self.action = AUTELIS_HEAT_TO_ACTION[heatMode]

        _LOGGER.info(f"Climate updated Temp: {self.current_temp} Target: {self.target_temp} Mode: {self.mode} Action: {self.action}")

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return self._icon