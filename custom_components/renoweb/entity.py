"""Shared Entity Definition for RenoWeb Integration."""
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.entity import Entity

from .const import DEFAULT_BRAND, DOMAIN


class RenoWebEntity(Entity):
    """Base class for RenoWeb Entities."""

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
        self._unique_id = f"{self.entity_object.replace(' ', '_')}_{self._address_id}"

    @property
    def name(self):
        """Return the name of the sensor."""
        name = self.entity_object.replace("-", " ")
        name = name.replace("_", " ")
        return f"{DOMAIN.capitalize()} {name}"

    @property
    def should_poll(self):
        """Poll entity to update attributes."""
        return False

    @property
    def device_info(self):
        return {
            "connections": {(dr.CONNECTION_NETWORK_MAC, self._address_id)},
            "manufacturer": DEFAULT_BRAND,
            "via_device": (DOMAIN, self._address_id),
        }

    @property
    def _data(self):
        """Return Data Object."""
        return self.coordinator.data.get(self.entity_object)

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
