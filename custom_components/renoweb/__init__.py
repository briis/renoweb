"""Support for the RenoWeb Garbage Collection Service."""
from __future__ import annotations

from datetime import timedelta
import logging
from types import MappingProxyType
from typing import Any, Self

from aiohttp.client_exceptions import ServerDisconnectedError
from pyrenoweb import (
    GarbageCollection,
    RenoWebCollectionData,
    RenowWebNotSupportedError,
    RenowWebNotValidAddressError,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError, ConfigEntryNotReady, Unauthorized
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_ADDRESS_ID,
    CONF_MUNICIPALITY,
    CONF_UPDATE_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

PLATFORMS = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up RenoWeb from a config entry."""

    coordinator = RenoWebtDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    config_entry.async_on_unload(config_entry.add_update_listener(async_update_entry))

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok

async def async_update_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Reload WeatherFlow Forecast component when options changed."""
    await hass.config_entries.async_reload(config_entry.entry_id)

class CannotConnect(HomeAssistantError):
    """Unable to connect to the web site."""

class RenoWebtDataUpdateCoordinator(DataUpdateCoordinator["RenoWebData"]):
    """Class to manage fetching RenoWeb data."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize global WeatherFlow forecast data updater."""
        self.renoweb = RenoWebData(
            hass, config_entry.data)
        self.renoweb.initialize_data()
        self.hass = hass
        self.config_entry = config_entry

        update_interval = timedelta(hours=self.config_entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_SCAN_INTERVAL))

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def _async_update_data(self) -> RenoWebData:
        """Fetch data from WeatherFlow Forecast."""
        try:
            return await self.renoweb.fetch_data()
        except Exception as err:
            raise UpdateFailed(f"Update failed: {err}") from err


class RenoWebData:
    """Keep data for RenoWeb."""

    def __init__(self, hass: HomeAssistant, config: MappingProxyType[str, Any]) -> None:
        """Initialise renoweb entity data."""

        self.hass = hass
        self._config = config
        self.renoweb_data: GarbageCollection
        self.collection_data: RenoWebCollectionData = []

    def initialize_data(self) -> bool:
        """Establish connection to API."""
        self.renoweb_data = GarbageCollection(
                municipality=self._config[CONF_MUNICIPALITY],
                session=async_get_clientsession(self.hass),
        )

        return True

    async def fetch_data(self) -> Self:
        """Fetch data from API."""

        try:
            resp: RenoWebCollectionData = await self.renoweb_data.get_data(address_id=self._config[CONF_ADDRESS_ID])
        except RenowWebNotSupportedError as err:
            _LOGGER.debug(err)
            return False
        except RenowWebNotValidAddressError as err:
            _LOGGER.debug(err)
            return False
        except err as notreadyerror:
            _LOGGER.debug(notreadyerror)
            raise ConfigEntryNotReady from notreadyerror

        if not resp:
            raise CannotConnect()

        self.collection_data = resp

        return self