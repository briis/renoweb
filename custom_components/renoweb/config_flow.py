"""Config Flow for Renoweb Integration."""

import logging
import voluptuous as vol

from pyrenoweb import (
    RenoWeb,
    RequestError,
    ResultError,
    InvalidApiKey,
    MunicipalityError,
)
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import (
    API_KEY_MUNICIPALITIES,
    API_KEY,
    CONF_ADDRESS,
    CONF_ADDRESS_ID,
    CONF_HOUSE_NUMBER,
    CONF_MUNICIPALITY,
    CONF_MUNICIPALITY_ID,
    CONF_ROAD_NAME,
    CONF_UPDATE_INTERVAL,
    CONF_ZIPCODE,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class RenoWebConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """RenoWeb configuration flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is None:
            return await self._show_setup_form()

        session = async_create_clientsession(self.hass)
        renoweb = RenoWeb(API_KEY_MUNICIPALITIES, API_KEY, session)

        try:
            unique_data = await renoweb.find_renoweb_ids(
                user_input[CONF_MUNICIPALITY],
                user_input[CONF_ZIPCODE],
                user_input[CONF_ROAD_NAME],
                user_input[CONF_HOUSE_NUMBER],
            )
        except MunicipalityError:
            errors["base"] = "municipality_not_supported"
            return await self._show_setup_form(errors)
        except ResultError:
            errors["base"] = "location_not_found"
            return await self._show_setup_form(errors)
        except InvalidApiKey:
            errors["base"] = "connection_error"
            return await self._show_setup_form(errors)
        except RequestError:
            errors["base"] = "request_error"
            return await self._show_setup_form(errors)

        address = unique_data.get("address")
        address_id = unique_data.get("address_id")
        municipality_id = unique_data.get("municipality_id")
        if user_input[CONF_MUNICIPALITY].isnumeric():
            municipality_name = unique_data.get("municipality")
        else:
            municipality_name = user_input[CONF_MUNICIPALITY]
        entries = self._async_current_entries()
        for entry in entries:
            if entry.data[CONF_ADDRESS_ID] == address_id:
                return self.async_abort(reason="name_exists")

        return self.async_create_entry(
            title=address,
            data={
                CONF_ADDRESS: address,
                CONF_ADDRESS_ID: address_id,
                CONF_MUNICIPALITY_ID: municipality_id,
                CONF_MUNICIPALITY: municipality_name,
                CONF_ZIPCODE: user_input.get(CONF_ZIPCODE),
                CONF_ROAD_NAME: user_input.get(CONF_ROAD_NAME),
                CONF_HOUSE_NUMBER: user_input.get(CONF_HOUSE_NUMBER),
                CONF_UPDATE_INTERVAL: user_input.get(CONF_UPDATE_INTERVAL),
            },
        )

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MUNICIPALITY): str,
                    vol.Required(CONF_ZIPCODE): str,
                    vol.Required(CONF_ROAD_NAME): str,
                    vol.Required(CONF_HOUSE_NUMBER): str,
                    vol.Optional(
                        CONF_UPDATE_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): vol.All(vol.Coerce(int), vol.Range(min=3, max=24)),
                }
            ),
            errors=errors or {},
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=3, max=24)),
                }
            ),
        )
