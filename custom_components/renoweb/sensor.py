"""Sensors for the RenoWeb Garbage Collection Service."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.typing import StateType

from .const import (
    ATTR_DAYS_TO,
    ATTR_ICON_COLOR,
    ATTR_SCHEDULE,
    ATTR_TYPE_ID,
    ATTR_VALID_DATA,
    DOMAIN,
)
from .entity import RenoWebEntity
from .models import RenoWebEntryData


@dataclass
class RenoWebRequiredKeysMixin:
    """Mixin for required keys."""

    always_add: bool


@dataclass
class RenoWebSensorEntityDescription(SensorEntityDescription, RenoWebRequiredKeysMixin):
    """Describes RenowWeb sensor."""


SENSOR_TYPES: tuple[RenoWebSensorEntityDescription, ...] = (
    RenoWebSensorEntityDescription(
        key="Restaffald-Madaffald",
        name="Rest- og Madaffald",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="PAPPI",
        name="Papir og Plastik",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Metal-Glas",
        name="Metal og Glas",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Farligt affald",
        name="Farligt affald",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Tekstiler",
        name="Tekstiler",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Jern",
        name="Jern",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Papir",
        name="Papir",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Pap",
        name="Pap",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Plast Metal",
        name="Plast og Metal",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Storskrald",
        name="Storskrald",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Haveaffald",
        name="Haveaffald",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Next Collection",
        name="Næste tømning",
        device_class=SensorDeviceClass.DATE,
        state_class=SensorStateClass.MEASUREMENT,
        always_add=True,
    ),
)

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

    entities = []
    for description in SENSOR_TYPES:
        if description.always_add or (
            f"{description.key}_{municipality_id}_{address_id}" in coordinator.data
        ):
            entities.append(
                RenoWebSensor(
                    coordinator,
                    renowebapi,
                    description,
                    municipality_id,
                    address_id,
                    entry,
                )
            )
    async_add_entities(entities)


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
        self._attr_name = f"{DOMAIN.capitalize()} {self.entity_description.name}"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.device_data["date"]

    @property
    def icon(self):
        """Return icon for the sensor."""
        return self.device_data["icon"]

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        return {
            **super().extra_state_attributes,
            ATTR_DAYS_TO: self.device_data["days_to"],
            ATTR_ICON_COLOR: self.device_data["icon_color"],
            ATTR_SCHEDULE: self.device_data["schedule"],
            ATTR_TYPE_ID: self.device_data["id"],
            ATTR_VALID_DATA: self.device_data["valid_data"],
        }
