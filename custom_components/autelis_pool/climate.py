# """Support for controlling Heaters through Autelis."""
import logging
import collections

import requests

from homeassistant.const import (
    ATTR_TEMPERATURE, 
    UnitOfTemperature
    )
from homeassistant.helpers.entity import Entity
from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
    )
from .const import DOMAIN, HEAT_SET, _LOGGER, MAX_TEMP, MIN_TEMP, STATE_AUTO

AUTELIS_HEAT_TO_ACTION = collections.OrderedDict(
    [
        (0, None),
        (1, HVACAction.IDLE),
        (2, HVACAction.HEATING),
    ]
)

AUTELIS_HEAT_TO_MODE = collections.OrderedDict(
    [
        (0, HVACMode.OFF),
        (1, HVACMode.HEAT),
        (2, HVACMode.HEAT),
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
        self._unit_of_measurement = UnitOfTemperature.FAHRENHEIT
        self._icon = icon
        self.mode = None
        self.action = None
        _LOGGER.debug("Created Autelis sensor %r", self)

    @property
    def unique_id(self):
        """Return a unique identifier for this autelis thermostat."""
        return f"autelis {self.data.host} {self.sensor_name}"

    @property
    def available(self):
        """Return if the switch is available to be turned on."""
        return self.data.mode == STATE_AUTO

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.friendly_name

    async def async_set_hvac_mode(self, hvac_mode):
        # _LOGGER.warn(f"Set Mode {hvac_mode} {self.mode}")
        self.mode = hvac_mode
        newMode = 1 if hvac_mode == HVACMode.HEAT else 0
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
        return ClimateEntityFeature.TARGET_TEMPERATURE

    @property
    def hvac_modes(self):
        return HVACMode.OFF, HVACMode.HEAT

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