"""Sensors for the RenoWeb Garbage Collection Service."""

import logging
from datetime import datetime
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
import homeassistant.util.dt as dt
from homeassistant.const import ATTR_ATTRIBUTION
from pyrenoweb import (
    TYPE_METAL_GLASS,
    TYPE_PAPER,
    TYPE_RESIDUAL,
    TYPE_PLASTIC,
    TYPE_STORSKRALD,
    TYPE_HAVEAFFALD,
    TYPE_GLASS,
)
from .const import (
    ATTR_DESCRIPTION,
    ATTR_NEXT_PICKUP_TEXT,
    ATTR_NEXT_PICKUP_DATE,
    ATTR_REFRESH_TIME,
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
        if self.entity_object in TYPE_RESIDUAL:
            return f"mdi:delete"
        elif self.entity_object in TYPE_PAPER:
            return f"mdi:file"
        elif self.entity_object in TYPE_METAL_GLASS:
            return f"mdi:bottle-wine"
        elif self.entity_object in TYPE_GLASS:
            return f"mdi:bottle-wine"
        elif self.entity_object in TYPE_HAVEAFFALD:
            return "mdi:tree"
        elif self.entity_object in TYPE_PLASTIC:
            return "mdi:cup"
        elif self.entity_object in TYPE_STORSKRALD:
            return "mdi:truck"
        else:
            return f"mdi:delete"

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        local_dt = dt.as_local(datetime.now())
        return {
            ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
            ATTR_DESCRIPTION: self.data.get("description"),
            ATTR_NEXT_PICKUP_TEXT: self.data.get("nextpickupdatetext"),
            ATTR_NEXT_PICKUP_DATE: self.data.get("nextpickupdate"),
            ATTR_REFRESH_TIME: local_dt.strftime("%d-%m-%Y %H:%M"),
            ATTR_SCHEDULE: self.data.get("schedule"),
        }
