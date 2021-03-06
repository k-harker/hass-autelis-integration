"""Support for Autelis switches"""
from homeassistant.components.switch import SwitchEntity

from .const import (_LOGGER, DOMAIN, CIRCUITS)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up autelis pump circuit switches."""
    data = hass.data[DOMAIN]
    entities  = []
    for item in CIRCUITS:
        entities .append(AutelisCircuit(data, item, CIRCUITS[item]))

    async_add_entities(entities , True)


class AutelisCircuit(SwitchEntity):
    """Representation of an Autelis pump."""
    def __init__(self, data, equipment_name, friendly_name):
        self.data = data
        self.api = data.api
        self._name = f"{equipment_name}"
        self.equipment_name = equipment_name
        self.friendly_name = friendly_name
        
        _LOGGER.debug(f"adding circuit for {equipment_name}")

    @property
    def name(self):
        """Return the name of the circuit."""
        return self.friendly_name

    @property
    def unique_id(self):
        """Return a unique identifier for this circuit."""
        return f"{self.data.host} {self.equipment_name}"

    @property
    def is_on(self):
        """Return true if switch is on."""

        return True if self.data.equipment[self.equipment_name] == "1" else False

    async def async_turn_on(self, **kwargs):
        """Turn on switch."""
        self.data.equipment[self.equipment_name] = "1"
        await self.api.control(self.equipment_name, 1)

    async def async_turn_off(self, **kwargs):
        """Turn off switch."""
        self.data.equipment[self.equipment_name] = "0"
        await self.api.control(self.equipment_name, 0)

