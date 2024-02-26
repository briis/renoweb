"""Support for the RenoWeb Garbage Collection Service."""
from __future__ import annotations

import logging
from datetime import timedelta

from aiohttp.client_exceptions import ServerDisconnectedError
from pyrenoweb import (
    GarbageCollection,
    RenoWebAddressInfo,
    RenoWebPickupData,
    RenowWebNotSupportedError,
    RenowWebNotValidAddressError,
)

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_KEY,
    CONF_ADDRESS,
    CONF_ADDRESS_ID,
    CONF_MUNICIPALITY_ID,
    CONF_UPDATE_INTERVAL,
    DEFAULT_API_VERSION,
    DEFAULT_BRAND,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    INTEGRATION_PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up RenoWeb platforms as config entry."""

    if not entry.options:
        hass.config_entries.async_update_entry(
            entry,
            options={
                CONF_UPDATE_INTERVAL: entry.data.get(
                    CONF_UPDATE_INTERVAL, DEFAULT_SCAN_INTERVAL
                ),
            },
        )

    session = aiohttp_client.async_get_clientsession(hass)
    renoweb = RenoWebData(
        API_KEY,
        entry.data.get(CONF_MUNICIPALITY_ID),
        entry.data.get(CONF_ADDRESS_ID),
        session,
    )
    _LOGGER.debug("Connected to RenoWeb Platform")

    try:
        await renoweb.get_pickup_data()
    except InvalidApiKey:
        _LOGGER.error(
            "Could not Authorize against RenowWeb. API Keys might have changed."
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
            data = await renoweb.get_pickup_data()
            return data
        except (RequestError, ResultError) as err:
            _LOGGER.error("Error occured: %s", err)
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
    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "renoweb": renoweb,
        "municipality_id": entry.data.get(CONF_MUNICIPALITY_ID),
        "address_id": entry.data.get(CONF_ADDRESS_ID),
    }

    await _async_get_or_create_renoweb_device_in_registry(
        hass, entry, entry.data.get(CONF_ADDRESS_ID)
    )
    await hass.config_entries.async_forward_entry_setups(entry, INTEGRATION_PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_options_updated))

    return True


async def _async_get_or_create_renoweb_device_in_registry(
    hass: HomeAssistant, entry: ConfigEntry, address_id
) -> None:
    device_registry = dr.async_get(hass)
    device_key = f"{address_id}"
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, device_key)},
        identifiers={(DOMAIN, device_key)},
        manufacturer=DEFAULT_BRAND,
        name=entry.data[CONF_ADDRESS],
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
