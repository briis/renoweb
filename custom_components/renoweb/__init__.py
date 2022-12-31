"""Support for the RenoWeb Garbage Collection Service."""
from __future__ import annotations

import logging
from datetime import timedelta

from aiohttp.client_exceptions import ServerDisconnectedError
from pyrenoweb import (
    RenoWebData,
    InvalidApiKey,
    RequestError,
    ResultError,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_KEY,
    CONFIG_OPTIONS,
    CONF_ADDRESS_ID,
    CONF_MUNICIPALITY_ID,
    CONF_UPDATE_INTERVAL,
    DEFAULT_API_VERSION,
    DEFAULT_BRAND,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    INTEGRATION_PLATFORMS,
)
from .models import RenoWebEntryData

_LOGGER = logging.getLogger(__name__)


@callback
def _async_import_options_from_data_if_missing(hass: HomeAssistant, entry: ConfigEntry):
    options = dict(entry.options)
    data = dict(entry.data)
    modified = False
    for importable_option in CONFIG_OPTIONS:
        if importable_option not in entry.options and importable_option in entry.data:
            options[importable_option] = entry.data[importable_option]
            del data[importable_option]
            modified = True

    if modified:
        hass.config_entries.async_update_entry(entry, data=data, options=options)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up RenoWeb platforms as config entry."""
    _async_import_options_from_data_if_missing(hass, entry)

    session = async_create_clientsession(hass)
    renowebapi = RenoWebData(
        API_KEY,
        entry.data.get(CONF_MUNICIPALITY_ID),
        entry.data.get(CONF_ADDRESS_ID),
        session,
    )
    _LOGGER.debug("Connected to RenoWeb Platform")

    try:
        await renowebapi.fetch_waste_data()
    except InvalidApiKey:
        _LOGGER.error(
            "Could not Authorize against Weatherflow Server. Please reinstall integration."
        )
        return False
    except (ResultError, ServerDisconnectedError) as err:
        _LOGGER.warning(str(err))
        raise ConfigEntryNotReady from err
    except RequestError as err:
        _LOGGER.error("Error occured: %s", err)
        raise ConfigEntryNotReady from err

    if entry.unique_id is None:
        hass.config_entries.async_update_entry(
            entry, unique_id=entry.data.get(CONF_ADDRESS_ID)
        )

    async def async_update_data():
        """Obtain the latest data from RenoWeb."""
        try:
            data = await renowebapi.fetch_waste_data()
            return data

        except (ResultError, ServerDisconnectedError) as err:
            raise UpdateFailed(f"Error while retreiving data: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(
            hours=entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_SCAN_INTERVAL)
        ),
    )
    await coordinator.async_config_entry_first_refresh()
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = RenoWebEntryData(
        coordinator=coordinator,
        renoweb=renowebapi,
        municipality_id=entry.data.get(CONF_MUNICIPALITY_ID),
        address_id=entry.data.get(CONF_ADDRESS_ID),
    )

    await _async_get_or_create_renoweb_device_in_registry(hass, entry)

    hass.config_entries.async_setup_platforms(entry, INTEGRATION_PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_options_updated))

    return True


async def _async_get_or_create_renoweb_device_in_registry(
    hass: HomeAssistantType, entry: ConfigEntry
) -> None:
    device_registry = dr.async_get(hass)

    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, entry.unique_id)},
        identifiers={(DOMAIN, entry.unique_id)},
        manufacturer=DEFAULT_BRAND,
        name=f"{DOMAIN.capitalize()} {entry.data.get(CONF_ADDRESS_ID)}",
        model=DEFAULT_BRAND,
        sw_version=DEFAULT_API_VERSION,
    )


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry):
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload WeatherFlow entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, INTEGRATION_PLATFORMS
    )
    return unload_ok
