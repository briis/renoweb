"""Binary Sensors for the RenoWeb Garbage Collection Service."""
from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .entity import RenoWebEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the RenoWeb sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator.data:
        return

    renoweb = hass.data[DOMAIN][entry.entry_id]["renoweb"]
    if not renoweb:
        return

    municipality_id = hass.data[DOMAIN][entry.entry_id]["municipality_id"]
    if not municipality_id:
        return

    address_id = hass.data[DOMAIN][entry.entry_id]["address_id"]
    if not address_id:
        return

    binary_sensors = []
    for binary_sensor in coordinator.data:
        if binary_sensor != "days_until_next_pickup":
            binary_sensors.append(
                RenoWebBinarySensor(
                    coordinator, renoweb, binary_sensor, municipality_id, address_id
                )
            )
            _LOGGER.debug("BINARY SENSOR ADDED: %s", binary_sensor)
    async_add_entities(binary_sensors, True)

    return True


class RenoWebBinarySensor(RenoWebEntity, BinarySensorEntity):
    """Implementation of a RenoWeb Sensor."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, coordinator, renoweb, sensor, municipality_id, address_id):
        """Initialize the sensor."""
        super().__init__(coordinator, renoweb, sensor, municipality_id, address_id)

        # _name = self._data.get("description").replace("-", " ")
        # _name = _name.replace("_", " ")
        self._attr_name = f"{DOMAIN.capitalize()} {self._data.get('name')} Valid"
        self._attr_unique_id = (
            f"{self.entity_object.replace(' ', '_')}_{self._address_id}_valid"
        )

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._data.get("data_valid", False)
