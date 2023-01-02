"""Shared Entity Definition for RenoWeb Integration."""
from __future__ import annotations

from homeassistant.const import ATTR_ATTRIBUTION
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.entity import DeviceInfo, Entity

from .const import DEFAULT_ATTRIBUTION, DEFAULT_BRAND, DOMAIN


class RenoWebEntity(Entity):
    """Base class for RenoWeb Entities."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(
        self, coordinator, renoweb, entity_object, municipality_id, address_id
    ):
        """Initialize the entity."""
        super().__init__()
        self.coordinator = coordinator
        self.renoweb = renoweb
        self.entity_object = entity_object
        self._address_id = address_id
        self._municipality_id = municipality_id
        self._attr_available = self.coordinator.last_update_success
        self._attr_device_info = DeviceInfo(
            manufacturer=DEFAULT_BRAND,
            connections={(dr.CONNECTION_NETWORK_MAC, self._address_id)},
            via_device=(DOMAIN, self._address_id),
        )

    @property
    def _data(self):
        """Return Data Object."""
        return self.coordinator.data.get(self.entity_object)

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
