"""Shared Entity Definition for RenoWeb Integration."""
from __future__ import annotations

import logging

import homeassistant.helpers.device_registry as dr
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from pyrenoweb import RenoWebSensorDescription

from .const import DOMAIN, DEFAULT_ATTRIBUTION

_LOGGER = logging.getLogger(__name__)


class RenoWebEntity(Entity):
    """Base class for RenoWeb Entities."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Seven is reasonable in this case.

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        renowebapi,
        entity_object: RenoWebSensorDescription,
        municipality_id,
        address_id,
        entries: ConfigEntry,
    ):
        """Initialize the entity."""
        super().__init__()

        self.coordinator = coordinator
        self.renowebapi = renowebapi
        self.entity_object = entity_object
        self.entry: ConfigEntry = entries
        self._address_id = address_id
        self._municipality_id = municipality_id

        self._attr_available = self.coordinator.last_update_success
        self._attr_unique_id = f"{municipality_id}_{self.entity_object.key}"
        self._attr_name = f"{DOMAIN.capitalize()} {self.entity_object.name}"

    @property
    def extra_state_attributes(self):
        """Return common attributes"""
        return {
            ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
        }

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    # @property
    # def name(self):
    #     """Return the name of the sensor."""

    #     name = self._data.get("description").replace("-", " ")
    #     name = name.replace("_", " ")
    #     return f"{DOMAIN.capitalize()} {name}"

    # @property
    # def should_poll(self):
    #     """Poll entity to update attributes."""
    #     return False

    # @property
    # def device_info(self):
    #     return {
    #         "connections": {(dr.CONNECTION_NETWORK_MAC, self._address_id)},
    #         "manufacturer": DEFAULT_BRAND,
    #         "via_device": (DOMAIN, self._address_id),
    #     }

    # @property
    # def _data(self):
    #     """Return Data Object."""
    #     return self.coordinator.data.get(self.entity_object)

    # @property
    # def unique_id(self):
    #     """Return a unique ID."""
    #     return self._unique_id

    # @property
    # def available(self):
    #     """Return if entity is available."""
    #     return self.coordinator.last_update_success

    # async def async_added_to_hass(self):
    #     """When entity is added to hass."""
    #     self.async_on_remove(
    #         self.coordinator.async_add_listener(self.async_write_ha_state)
    #     )
