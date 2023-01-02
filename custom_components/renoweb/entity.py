"""Shared Entity Definition for RenoWeb Integration."""
from __future__ import annotations

import logging

import homeassistant.helpers.device_registry as dr
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from pyrenoweb import RenoWebDataSet, RenowWebDataItem

from .const import DOMAIN, DEFAULT_ATTRIBUTION, DEFAULT_BRAND

_LOGGER = logging.getLogger(__name__)


class RenoWebEntity(Entity):
    """Base class for RenoWeb Entities."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Seven is reasonable in this case.

    # _attr_has_entity_name = True

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
        # _LOGGER.debug("DATA: %s", self.coordinator.data)
        self.entity_item = (
            f"{self.entity_description.key}_{municipality_id}_{address_id}"
        )
        # self.device_data: RenowWebDataItem = coordinator.data[
        #     f"{self.entity_description.key}_{municipality_id}_{address_id}"
        # ]
        _LOGGER.debug("KEY: %s", self.entity_item)
        _LOGGER.debug("DATA: %s", self.coordinator.data)
        self.entity_item = "Restaffald-Madaffald_0265_85146"
        self.device_data: RenowWebDataItem = getattr(
            self.coordinator.data, self.entity_item
        )
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
        )
        _LOGGER.debug("DATA: %s", self.coordinator.data)

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
