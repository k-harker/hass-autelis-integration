"""Support for Autelis sensors."""

from homeassistant.const import (
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    TEMP_FAHRENHEIT,
    PERCENTAGE,
)
from homeassistant.helpers.entity import Entity

from .const import _LOGGER, DOMAIN, TEMP_SENSORS



async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up autelis temperature sensors."""
    data = hass.data[DOMAIN]
    dev = []
    for item in TEMP_SENSORS.items():
        dev.append(AutelisSensor(data, item[0], item[1][0]))

    async_add_entities(dev, True)


class AutelisSensor(Entity):
    """Representation of an Autelis sensor."""

    def __init__(self, data, sensor_name, sensor_type):
        """Initialize the sensor."""
        self.data = data
        self._name = f"{sensor_name} {sensor_type}"
        self.sensor_name = sensor_name
        self.type = sensor_type
        self._state = None
        self._unit_of_measurement = TEMP_FAHRENHEIT

        _LOGGER.debug(f"adding sensor {sensor_name}")

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique identifier for this sensor."""
        return f"{self.data.host} {self.sensor_name}"
                

    # @property
    # def device_info(self):
    #     """Return device information for this sensor."""
    #     identifier = None
    #     model = None
    #     for sensor in self.data.ecobee.get_remote_sensors(self.index):
    #         if sensor["name"] != self.sensor_name:
    #             continue
    #         if "code" in sensor:
    #             identifier = sensor["code"]
    #             model = "ecobee Room Sensor"
    #         else:
    #             thermostat = self.data.ecobee.get_thermostat(self.index)
    #             identifier = thermostat["identifier"]
    #             try:
    #                 model = (
    #                     f"{ECOBEE_MODEL_TO_NAME[thermostat['modelNumber']]} Thermostat"
    #                 )
    #             except KeyError:
    #                 _LOGGER.error(
    #                     "Model number for ecobee thermostat %s not recognized. "
    #                     "Please visit this link and provide the following information: "
    #                     "https://github.com/home-assistant/home-assistant/issues/27172 "
    #                     "Unrecognized model number: %s",
    #                     thermostat["name"],
    #                     thermostat["modelNumber"],
    #                 )
    #         break

    #     if identifier is not None and model is not None:
    #         return {
    #             "identifiers": {(DOMAIN, identifier)},
    #             "name": self.sensor_name,
    #             "manufacturer": MANUFACTURER,
    #             "model": model,
    #         }
    #     return None

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        if self.type in (DEVICE_CLASS_TEMPERATURE):
            return self.type
        return None

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._state in ["unknown"]:
            return None

        if self.type == "temperature":
            return float(self._state) / 10

        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement this sensor expresses itself in."""
        return self._unit_of_measurement

    async def async_update(self):
        """Get the latest state of the sensor."""
        await self.data.update()

        self._state = self.data.sensors[self.sensor_name]
