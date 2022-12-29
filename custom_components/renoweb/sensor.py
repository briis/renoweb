"""Sensors for the RenoWeb Garbage Collection Service."""
from __future__ import annotations

import logging
from datetime import datetime
from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util.dt import dt
from homeassistant.const import ATTR_ATTRIBUTION
from pyrenoweb import (
    RenoWebSensorDescription,
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
    ATTR_FORMATTED_STATE_DK,
    ATTR_NEXT_PICKUP_TEXT,
    ATTR_NEXT_PICKUP_DATE,
    ATTR_REFRESH_TIME,
    ATTR_SHORT_STATE_DK,
    ATTR_SCHEDULE,
    DEFAULT_ATTRIBUTION,
    DOMAIN,
)
from .entity import RenoWebEntity
from .models import RenoWebEntryData

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the RenoWeb sensor platform."""
    entry_data: RenoWebEntryData = hass.data[DOMAIN][entry.entry_id]
    renowebapi = entry_data.renoweb
    coordinator = entry_data.coordinator
    municipality_id = entry_data.municipality_id
    address_id = entry_data.address_id
    # if not coordinator.data:
    #     return

    # renowebapi = hass.data[DOMAIN][entry.entry_id]["renoweb"]
    # if not renoweb:
    #     return

    # municipality_id = hass.data[DOMAIN][entry.entry_id]["municipality_id"]
    # if not municipality_id:
    #     return

    # address_id = hass.data[DOMAIN][entry.entry_id]["address_id"]
    # if not address_id:
    #     return

    sensors = []
    for sensor in coordinator.data:
        _LOGGER.debug("SENSOR ADDED: %s", sensor)
        sensors.append(
            RenoWebSensor(
                coordinator,
                renowebapi,
                sensor,
                municipality_id,
                address_id,
                entry,
            )
        )
    async_add_entities(sensors)

    return True


class RenoWebSensor(RenoWebEntity, SensorEntity):
    """Implementation of a RenoWeb Sensor."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(
        self,
        coordinator,
        renowebapi,
        sensor,
        municipality_id,
        address_id,
        entries: ConfigEntry,
    ):
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            renowebapi,
            sensor,
            municipality_id,
            address_id,
            entries,
        )

    # @property
    # def state(self):
    #     """Return the state of the sensor."""
    #     return self._data.get("daysuntilpickup")

    # @property
    # def unit_of_measurement(self):
    #     """Return the unit of measurement."""
    #     return "dage"

    # @property
    # def icon(self):
    #     """Icon to use in the frontend."""
    #     _type = self.entity_object
    #     _type_idx = _type.rfind("_")
    #     garbage_type = _type[0:_type_idx].replace("_", " ")
    #     if garbage_type in TYPE_RESIDUAL:
    #         return "mdi:delete"
    #     if garbage_type in TYPE_PAPER:
    #         return "mdi:file"
    #     if garbage_type in TYPE_METAL_GLASS:
    #         return "mdi:bottle-wine"
    #     if garbage_type in TYPE_GLASS:
    #         return "mdi:bottle-wine"
    #     if garbage_type in TYPE_HAVEAFFALD:
    #         return "mdi:tree"
    #     if garbage_type in TYPE_PLASTIC:
    #         return "mdi:cup"
    #     if garbage_type in TYPE_STORSKRALD:
    #         return "mdi:truck"

    #     return "mdi:delete"

    # @property
    # def extra_state_attributes(self):
    #     """Return the state attributes of the device."""
    #     local_dt = dt.now()
    #     pickup_dt = datetime.fromtimestamp(
    #         int(self._data.get("nextpickupdatetimestamp"))
    #     )
    #     day_number = pickup_dt.weekday()
    #     day_list = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"]
    #     day_name = day_list[day_number]
    #     format_dt = pickup_dt.strftime(" d. %d/%m")
    #     day_str = "dag" if self.state == 1 else "dage"
    #     format_state = (
    #         str(self.state) + " " + day_str + " (" + day_name + format_dt + ")"
    #     )
    #     short_state_dk = day_name + format_dt
    #     # Rewrite Attributes if no pickup schedule is supplied
    #     if self.state == -1:
    #         format_state = "Ikke Planlagt"
    #         short_state_dk = "Ikke Planlagt"
    #     return {
    #         ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
    #         ATTR_DESCRIPTION: self._data.get("description"),
    #         ATTR_NEXT_PICKUP_TEXT: self._data.get("nextpickupdatetext"),
    #         ATTR_NEXT_PICKUP_DATE: self._data.get("nextpickupdate"),
    #         ATTR_REFRESH_TIME: local_dt.strftime("%d-%m-%Y %H:%M"),
    #         ATTR_SCHEDULE: self._data.get("schedule"),
    #         ATTR_FORMATTED_STATE_DK: format_state,
    #         ATTR_SHORT_STATE_DK: short_state_dk,
    #     }
