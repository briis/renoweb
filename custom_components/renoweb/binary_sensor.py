"""RenoWeb Binary Sensors for Home Assistant"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, RenoWebRequiredKeysMixin
from .entity import RenoWebEntity
from .models import RenoWebEntryData

_LOGGER = logging.getLogger(__name__)


@dataclass
class RenoWebSensorEntityDescription(
    BinarySensorEntityDescription, RenoWebRequiredKeysMixin
):
    """Describes RenowWeb binary sensor."""


BINARY_SENSOR_TYPES: tuple[RenoWebSensorEntityDescription, ...] = (
    RenoWebSensorEntityDescription(
        key="Restaffald-Madaffald",
        name="Rest og Madaffald Valid",
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="PAPPI",
        name="Papir og Plastik Valid",
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Metal-Glas",
        name="Metal og Glas Valid",
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Farligt affald",
        name="Farligt affald Valid",
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Tekstiler",
        name="Tekstiler Valid",
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Jern",
        name="Jern Valid",
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Papir",
        name="Papir Valid",
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Pap",
        name="Pap Valid",
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Plast Metal",
        name="Plast og Metal Valid",
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Storskrald",
        name="Storskrald Valid",
        always_add=False,
    ),
    RenoWebSensorEntityDescription(
        key="Haveaffald",
        name="Haveaffald Valid",
        always_add=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the RenoWeb sensor platform."""
    entry_data: RenoWebEntryData = hass.data[DOMAIN][entry.entry_id]
    renowebapi = entry_data.renoweb
    coordinator = entry_data.coordinator
    municipality_id = entry_data.municipality_id
    address_id = entry_data.address_id

    entities = []
    for description in BINARY_SENSOR_TYPES:
        if description.always_add or (
            f"{description.key}_{municipality_id}_{address_id}" in coordinator.data
        ):
            entities.append(
                RenoWebBinarySensor(
                    coordinator,
                    renowebapi,
                    description,
                    municipality_id,
                    address_id,
                    entry,
                )
            )
    async_add_entities(entities)


class RenoWebBinarySensor(RenoWebEntity, BinarySensorEntity):
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

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self.device_data["valid_data"]

    @property
    def icon(self):
        """Return icon for the sensor."""
        return self.device_data["icon"]
