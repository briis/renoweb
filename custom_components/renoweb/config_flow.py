"""Config Flow for Renoweb Integration."""

import logging
import voluptuous as vol

from pyrenoweb import (
    RenoeWeb,
    RequestError,
    ResultError,
    InvalidApiKey,
)
from homeassistant import config_entries, core
from homeassistant.core import callback

from .const import (
    API_KEY_MUNICIPALITIES,
    API_KEY,
    CONF_ADDRESS_ID,
    CONF_HOUSE_NUMBER,
    CONF_MUNICIPALITY,
    CONF_MUNICIPALITY_ID,
    CONF_ROAD_NAME,
    CONF_UPDATE_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.
    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    renoweb = RenoeWeb(API_KEY_MUNICIPALITIES, API_KEY)

    try:
        unique_data = await renoweb.find_renoweb_ids(
            data[CONF_MUNICIPALITY], data[CONF_ROAD_NAME], data[CONF_HOUSE_NUMBER]
        )
        return unique_data
    except ResultError as error:
        return error


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
        info = None

        if user_input is not None:
            await self.async_set_unique_id(f"{user_input[CONF_ADDRESS_ID]}")
            self._abort_if_unique_id_configured()
            try:
                info = await validate_input(self.hass, user_input)
            except ResultError:
                errors = {"base": "connection_error"}

            if "base" not in errors and info is not None:
                address = info.get("address")
                address_id = info.get("id")
                municipality_id = info.get("municipality_id")
                return self.async_create_entry(
                    title=address,
                    data={
                        CONF_ADDRESS_ID: address_id,
                        CONF_MUNICIPALITY_ID: municipality_id,
                        CONF_MUNICIPALITY: user_input[CONF_MUNICIPALITY],
                        CONF_ROAD_NAME: user_input.get(CONF_ROAD_NAME),
                        CONF_HOUSE_NUMBER: user_input.get(CONF_HOUSE_NUMBER),
                        CONF_UPDATE_INTERVAL: user_input.get(CONF_UPDATE_INTERVAL),
                    },
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MUNICIPALITY): str,
                    vol.Required(CONF_ROAD_NAME): str,
                    vol.Required(CONF_HOUSE_NUMBER): str,
                    vol.Optional(
                        CONF_UPDATE_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): vol.All(vol.Coerce(int), vol.Range(min=3, max=24)),
                }
            ),
            errors=errors,
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
