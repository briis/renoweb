"""Support for Renoweb sensor data."""
from __future__ import annotations

import logging

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util.dt import utc_from_timestamp
from homeassistant.util.unit_system import METRIC_SYSTEM

from . import RenoWebtDataUpdateCoordinator
from .const import (
    ATTR_DESCRIPTION,
    CONF_ADDRESS_ID,
    DEFAULT_API_VERSION,
    DEFAULT_ATTRIBUTION,
    DEFAULT_BRAND,
    DOMAIN,
)
from pyrenoweb import ICON_LIST, NAME_LIST

@dataclass
class RenoWebSensorEntityDescription(SensorEntityDescription):
    """Describes RenoWeb sensor entity."""

SENSOR_TYPES: tuple[RenoWebSensorEntityDescription, ...] = (
    RenoWebSensorEntityDescription(
        key="restaffaldmadaffald",
        name="Rest- & madaffald",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="restmad",
        name="Rest- & madaffald",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="dagrenovation",
        name="Dagrenovations",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="metalglas",
        name="Metal & Glas",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="pappi",
        name="Papir & Plast",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="farligtaffald",
        name="Farligt affald",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="farligtaffaldmiljoboks",
        name="Farligt affald & Miljøboks",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="flis",
        name="Flis",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="tekstiler",
        name="Tekstiler",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="jern",
        name="Jern",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="papir",
        name="Papir",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="papirmetal",
        name="Papir & Metal",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="pap",
        name="Pap",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="plastmetal",
        name="Plast & Metal",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="storskrald",
        name="Storskrald",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="storskraldogtekstilaffald",
        name="Storskrald & Tekstilaffald",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="haveaffald",
        name="Haveaffald",
        device_class=SensorDeviceClass.DATE,
    ),
    RenoWebSensorEntityDescription(
        key="next_pickup",
        name="Næste afhentning",
        device_class=SensorDeviceClass.DATE,
    ),
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """RenoWeb sensor platform."""
    coordinator: RenoWebtDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    if coordinator.data.collection_data == {}:
        return


    entities: list[RenoWebSensor[Any]] = [
        RenoWebSensor(coordinator, description, config_entry)
        for description in SENSOR_TYPES if getattr(coordinator.data.collection_data, description.key) is not None
    ]

    async_add_entities(entities, False)

class RenoWebSensor(CoordinatorEntity[DataUpdateCoordinator], SensorEntity):
    """A RenoWeb sensor."""

    entity_description: RenoWebSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: RenoWebtDataUpdateCoordinator,
        description: RenoWebSensorEntityDescription,
        config: MappingProxyType[str, Any]
    ) -> None:
        """Initialize a RenoWeb sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._config = config
        self._coordinator = coordinator

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._config.data[CONF_ADDRESS_ID])},
            entry_type=DeviceEntryType.SERVICE,
            manufacturer=DEFAULT_BRAND,
            model=DEFAULT_API_VERSION,
            name=f"{DOMAIN.capitalize()} Sensors",
            configuration_url=f"https://github.com/briis/renoweb",
        )
        self._attr_attribution = DEFAULT_ATTRIBUTION
        self._attr_unique_id = f"{config.data[CONF_ADDRESS_ID]} {description.key}"

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return unit of sensor."""

        return super().native_unit_of_measurement

    @property
    def native_value(self) -> StateType:
        """Return state of the sensor."""

        return (
            getattr(self._coordinator.data.collection_data, self.entity_description.key)
            if self._coordinator.data.collection_data else None
        )

    @property
    def icon(self) -> str | None:
        """Return icon for sensor."""
        if self.entity_description.key == "next_pickup":
            return ICON_LIST.get(self._coordinator.data.collection_data.next_pickup_item)

        return ICON_LIST.get(self.entity_description.key)

    @property
    def extra_state_attributes(self) -> None:
        """Return non standard attributes."""

        if self.entity_description.key == "next_pickup":
            return {
                ATTR_DESCRIPTION: NAME_LIST.get(self._coordinator.data.collection_data.next_pickup_item),
            }


    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )

