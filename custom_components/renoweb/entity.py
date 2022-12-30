"""Shared Entity Definition for RenoWeb Integration."""
from __future__ import annotations

import logging

import homeassistant.helpers.device_registry as dr
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


from .const import DOMAIN, DEFAULT_ATTRIBUTION, DEFAULT_BRAND

_LOGGER = logging.getLogger(__name__)


class RenoWebEntity(Entity):
    """Base class for RenoWeb Entities."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Seven is reasonable in this case.

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        renowebapi,
        description,
        municipality_id,
        address_id,
        entries: ConfigEntry,
    ):
        """Initialize the entity."""
        super().__init__()

        if description:
            self.entity_description = description

        self.coordinator = coordinator
        self.device_data = coordinator.data[
            f"{self.entity_description.key}_{municipality_id}_{address_id}"
        ]
        self.renowebapi = renowebapi
        self.entry: ConfigEntry = entries
        self._address_id = address_id
        self._municipality_id = municipality_id

        self._attr_available = self.coordinator.last_update_success
        self._attr_unique_id = f"{municipality_id}_{self.entity_description.key}"
        self._attr_name = f"{self.entity_description.name}"

        self._attr_device_info = DeviceInfo(
            manufacturer=DEFAULT_BRAND,
            via_device=(DOMAIN, self.entry.unique_id),
            connections={(dr.CONNECTION_NETWORK_MAC, self.entry.unique_id)},
            configuration_url="https://www.borger.dk/Handlingsside?selfserviceId=cc9b93ae-81a8-4440-9e32-685f7a20c418&referringPageId=4d3a4fca-6adb-4c14-81d9-3b4ca89c1f91&type=DK",
        )

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
