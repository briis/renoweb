"""Sensors for the RenoWeb Garbage Collection Service."""
from __future__ import annotations

import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import datetime as dt
from homeassistant.core import HomeAssistant

from .const import (
    ATTR_DATA_VALID,
    ATTR_DESCRIPTION,
    ATTR_FORMATTED_STATE_DK,
    ATTR_ICON_COLOR,
    ATTR_NEXT_PICKUP_TEXT,
    ATTR_NEXT_PICKUP_DATE,
    ATTR_REFRESH_TIME,
    ATTR_SHORT_STATE_DK,
    ATTR_SCHEDULE,
    ATTR_STATE_TEXT,
    DOMAIN,
)
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

    sensors = []
    for sensor in coordinator.data:
        sensors.append(
            RenoWebSensor(coordinator, renoweb, sensor, municipality_id, address_id)
        )
        _LOGGER.debug("SENSOR ADDED: %s", sensor)
    async_add_entities(sensors, True)

    return True


class RenoWebSensor(RenoWebEntity, SensorEntity):
    """Implementation of a RenoWeb Sensor."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, coordinator, renoweb, sensor, municipality_id, address_id):
        """Initialize the sensor."""
        super().__init__(coordinator, renoweb, sensor, municipality_id, address_id)

        # _name = self._data.get("description").replace("-", " ")
        # _name = _name.replace("_", " ")
        self._attr_name = f"{DOMAIN.capitalize()} {self._data.get('name')}"
        self._attr_native_unit_of_measurement = "dage"
        self._attr_unique_id = (
            f"{self.entity_object.replace(' ', '_')}_{self._address_id}"
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._data.get("daysuntilpickup")

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return self._data.get("icon")

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        local_dt = dt.now()
        pickup_dt = datetime.fromtimestamp(
            int(self._data.get("nextpickupdatetimestamp"))
        )
        day_number = pickup_dt.weekday()
        day_list = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"]
        day_name = day_list[day_number]
        format_dt = pickup_dt.strftime(" d. %d/%m")
        day_str = "dag" if self.state == 1 else "dage"
        format_state = (
            str(self.state) + " " + day_str + " (" + day_name + format_dt + ")"
        )
        short_state_dk = day_name + format_dt
        # Rewrite Attributes if no pickup schedule is supplied
        if self.state == -1:
            format_state = "Ikke Planlagt"
            short_state_dk = "Ikke Planlagt"
        return {
            **super().extra_state_attributes,
            ATTR_DATA_VALID: self._data.get("data_valid"),
            ATTR_DESCRIPTION: self._data.get("description"),
            ATTR_ICON_COLOR: self._data.get("icon_color"),
            ATTR_NEXT_PICKUP_TEXT: self._data.get("nextpickupdatetext"),
            ATTR_NEXT_PICKUP_DATE: self._data.get("nextpickupdate"),
            ATTR_REFRESH_TIME: local_dt.strftime("%d-%m-%Y %H:%M"),
            ATTR_SCHEDULE: self._data.get("schedule"),
            ATTR_FORMATTED_STATE_DK: format_state,
            ATTR_SHORT_STATE_DK: short_state_dk,
            ATTR_STATE_TEXT: self._data.get("state_text"),
        }
