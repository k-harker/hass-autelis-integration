from homeassistant.helpers import aiohttp_client
from aiohttp import BasicAuth
import asyncio

from xml.etree import ElementTree

from .const import _LOGGER, DOMAIN, TEMP_SENSORS, AUTELIS_USERNAME



class AutelisPoolAPI:
    """Simple XML wrapper for Autelis's API."""

    def __init__(self,hass, api_url, password):
        """Initialize Autelis API and set params needed later."""
        self.api_url = api_url
        self.password = password
        self.available = False
        self.error_logged = False
        self.session = aiohttp_client.async_get_clientsession(hass)

    async def get(self, endpoint):
        """Send a get request, and return the response as a dict."""
        # Only query the API at most every 30 seconds
        
        kwargs = {}
        if self.password is not None:
            kwargs = {"auth": BasicAuth(AUTELIS_USERNAME, password=self.password)}
        
        url = self.api_url + endpoint
        try:
            response = await self.session.get(url, **kwargs)
            response.raise_for_status()
            
            self.available = True
            self.error_logged = False

            text = await response.text()

            # _LOGGER.error(text)

            return ElementTree.fromstring(text)
        except Exception as conn_exc:  # pylint: disable=broad-except
            log_string = "Failed to get Autelis Pool status. Error: %s" % conn_exc
            
            # Only log the first failure
            if not self.error_logged:
                log_string = f"Endpoint: {endpoint} {log_string}"
                _LOGGER.error(log_string)
            
            self.error_logged = True
            self.available = False
            return None

    async def get_status(self, group, name):
        
        status = await self.get("status.xml")
        
        if status is not None:
            return status.find(group).find(name).text
        return None

    async def control(self, equipment_name, attr_value, attr_name="value"):
        """Set the value for equipment_name."""
        endpoint = f"set.cgi?name={equipment_name}&{attr_name}={attr_value}"
        url = self.api_url + endpoint

        _LOGGER.error(url)

        kwargs = {}
        if self.password is not None:
            kwargs = {"auth": BasicAuth(AUTELIS_USERNAME, password=self.password)}
         
        try:
            response = await self.session.get(url, **kwargs)
            response.raise_for_status()

            self.available = True
            self.error_logged = False
        except Exception as conn_exc:  # pylint: disable=broad-except
            log_string = "Failed to send Autelis Pool command. Error: %s" % conn_exc
            
            # Only log the first failure
            if not self.error_logged:
                log_string = f"Endpoint: {endpoint} {log_string}"
                _LOGGER.error(log_string)
            
            self.error_logged = True
            self.available = False
            return None

        _LOGGER.info("Response", response)

        if response is not None:
            text = await response.text()
            _LOGGER.error(text)
            return text == "1"
        
        return response

