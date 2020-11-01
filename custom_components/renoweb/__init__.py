"""Support for the RenoWeb Garbage Collection Service."""

import asyncio
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
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

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


async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up configured RenoWeb."""
    # We allow setup only through config flow type of config
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
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

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = renoweb

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=renoweb.get_pickup_data,
        update_interval=timedelta(
            hours=entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_SCAN_INTERVAL)
        ),
    )

    try:
        await renoweb.get_pickup_data()
    except InvalidApiKey:
        _LOGGER.error(
            "Could not Authorize against Weatherflow Server. Please reinstall integration."
        )
        return
    except (ResultError, ServerDisconnectedError) as err:
        _LOGGER.warning(str(err))
        raise ConfigEntryNotReady
    except RequestError as err:
        _LOGGER.error(f"Error occured: {err}")
        return

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "renoweb": renoweb,
        "municipality_id": entry.data.get(CONF_MUNICIPALITY_ID),
        "address_id": entry.data.get(CONF_ADDRESS_ID),
    }

    await _async_get_or_create_renoweb_device_in_registry(
        hass, entry, entry.data.get(CONF_ADDRESS_ID)
    )

    for platform in INTEGRATION_PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    if not entry.update_listeners:
        entry.add_update_listener(async_update_options)

    return True


async def _async_get_or_create_renoweb_device_in_registry(
    hass: HomeAssistantType, entry: ConfigEntry, address_id
) -> None:
    device_registry = await dr.async_get_registry(hass)
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


async def async_update_options(hass: HomeAssistantType, entry: ConfigEntry):
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Unload Unifi Protect config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in INTEGRATION_PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
