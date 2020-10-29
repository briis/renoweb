"""Sensors for the RenoWeb Garbage Collection Service."""

import logging

from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
import homeassistant.helpers.device_registry as dr
from homeassistant.const import ATTR_ATTRIBUTION
from pyrenoweb import TYPE_METAL_GLASS, TYPE_PAPER, TYPE_RESIDUAL
from .const import (
    ATTR_DESCRIPTION,
    ATTR_NEXT_PICKUP_TEXT,
    ATTR_NEXT_PICKUP_DATE,
    ATTR_SCHEDULE,
    DEFAULT_ATTRIBUTION,
    DOMAIN,
    UNIT_SENSOR,
)
from .entity import RenoWebEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
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

    sensors = []
    for sensor in coordinator.data:
        sensors.append(
            RenoWebSensor(coordinator, renoweb, sensor, municipality_id, address_id)
        )
        _LOGGER.debug(f"SENSOR ADDED: {sensor}")
    async_add_entities(sensors, True)

    return True


class RenoWebSensor(RenoWebEntity, Entity):
    """ Implementation of a RenoWeb Sensor. """

    def __init__(self, coordinator, renoweb, sensor, municipality_id, address_id):
        """Initialize the sensor."""
        super().__init__(coordinator, renoweb, sensor, municipality_id, address_id)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.data.get("daysuntilpickup")

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return UNIT_SENSOR

    @property
    def icon(self):
        """Icon to use in the frontend."""
        if self.entity_object == TYPE_RESIDUAL:
            return f"mdi:delete"
        elif self.entity_object == TYPE_PAPER:
            return f"mdi:file"
        elif self.entity_object == TYPE_METAL_GLASS:
            return f"mdi:cup"
        else:
            return f"mdi:delete"

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return {
            ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
            ATTR_DESCRIPTION: self.data.get("description"),
            ATTR_NEXT_PICKUP_TEXT: self.data.get("nextpickupdatetext"),
            ATTR_NEXT_PICKUP_DATE: self.data.get("nextpickupdate"),
            ATTR_SCHEDULE: self.data.get("schedule"),
        }
