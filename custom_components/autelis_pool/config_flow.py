from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_HOST,
    CONF_NAME
)

import voluptuous as vol

from .const import DOMAIN

class AutelisFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Autelis config flow."""

    async def async_step_user(self, user_input):
        if user_input is not None:
            return self.async_create_entry(title=DOMAIN, data=user_input)

        schema = { 
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PASSWORD): str, 
        }
        errors = {}

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(schema),
            errors=errors
        )
