"""Support for Renoweb sensor data."""
from __future__ import annotations

import logging

from dataclasses import dataclass
from datetime import datetime as dt
from types import MappingProxyType
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import ATTR_DATE, ATTR_NAME, ATTR_ENTITY_PICTURE
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import RenoWebtDataUpdateCoordinator
from .const import (
    ATTR_DATE_LONG,
    ATTR_DESCRIPTION,
    ATTR_DURATION,
    ATTR_LAST_UPDATE,
    CONF_ADDRESS_ID,
    CONF_HOUSE_NUMBER,
    CONF_ROAD_NAME,
    DEFAULT_ATTRIBUTION,
    DEFAULT_BRAND,
    DOMAIN,
)
from pyrenoweb import ICON_LIST, PickupType

@dataclass
class RenoWebSensorEntityDescription(SensorEntityDescription):
    """Describes RenoWeb sensor entity."""

SENSOR_TYPES: tuple[RenoWebSensorEntityDescription, ...] = (
    RenoWebSensorEntityDescription(
        key="restaffaldmadaffald",
        name="Rest- & madaffald",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="glas",
        name="Glas",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="dagrenovation",
        name="Dagrenovations",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="metalglas",
        name="Metal & Glas",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="papirglas",
        name="Papir, Pap & Glas",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="pappi",
        name="Papir & Plast",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="farligtaffald",
        name="Farligt affald",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="farligtaffaldmiljoboks",
        name="Farligt affald & Miljøboks",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="flis",
        name="Flis",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="genbrug",
        name="Genbrug",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="jern",
        name="Jern",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="papir",
        name="Papir",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="papirmetal",
        name="Papir & Metal",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="pap",
        name="Pap",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="plastmetal",
        name="Plast & Metal",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="storskrald",
        name="Storskrald",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="storskraldogtekstilaffald",
        name="Storskrald & Tekstilaffald",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="haveaffald",
        name="Haveaffald",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="pappapirglasmetal",
        name="Pap, Papir, Glas & Metal",
        native_unit_of_measurement="dage",
    ),
    RenoWebSensorEntityDescription(
        key="next_pickup",
        name="Næste afhentning",
        native_unit_of_measurement="dage",
    ),
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """RenoWeb sensor platform."""
    coordinator: RenoWebtDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    if coordinator.data.pickup_events == {}:
        return


    entities: list[RenoWebSensor[Any]] = [
        RenoWebSensor(coordinator, description, config_entry)
        for description in SENSOR_TYPES if coordinator.data.pickup_events.get(description.key) is not None
    ]

    async_add_entities(entities, False)

class RenoWebSensor(CoordinatorEntity[DataUpdateCoordinator], SensorEntity):
    """A RenoWeb sensor."""

    entity_description: RenoWebSensorEntityDescription
    _attr_attribution = DEFAULT_ATTRIBUTION
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
        self._pickup_events: PickupType = coordinator.data.pickup_events.get(description.key) if coordinator.data.pickup_events else None

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._config.data[CONF_ADDRESS_ID])},
            entry_type=DeviceEntryType.SERVICE,
            manufacturer=DEFAULT_BRAND,
            name=f"{DOMAIN.capitalize()} {self._config.data[CONF_ROAD_NAME]} {self._config.data[CONF_HOUSE_NUMBER]}",
            configuration_url="https://github.com/briis/renoweb",
        )
        self._attr_unique_id = f"{config.data[CONF_ADDRESS_ID]} {description.key}"

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return unit of sensor."""

        current_time = dt.today()
        pickup_time: dt = self._pickup_events.date
        if pickup_time:
            if ((pickup_time - current_time).days + 1) == 1:
                return "dag"

        return super().native_unit_of_measurement

    @property
    def native_value(self) -> StateType:
        """Return state of the sensor."""

        current_time = dt.today()
        pickup_time: dt = self._pickup_events.date
        if pickup_time:
            return (pickup_time - current_time).days + 1

    @property
    def icon(self) -> str | None:
        """Return icon for sensor."""

        return ICON_LIST.get(self.entity_description.key)

    @property
    def extra_state_attributes(self) -> None:
        """Return non standard attributes."""

        _date: dt = self._pickup_events.date
        _current_date = dt.today()
        _state = (_date - _current_date).days + 1
        _day_number = _date.weekday()
        _weekdays = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"]
        _weekdays_full = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
        _day_name = _weekdays[_day_number]
        _day_name_long = _weekdays_full[_day_number]
        if _state == 0:
            _day_text = "I dag"
        elif _state == 1:
            _day_text = "I morgen"
        else:
            _day_text = f"Om {_state} dage"

        return {
            ATTR_DATE: _date.date() if _date else None,
            ATTR_DATE_LONG: f"{_day_name_long} {_date.strftime("d. %d-%m-%Y") if _date else None}" ,
            ATTR_DESCRIPTION: self._pickup_events.description,
            ATTR_DURATION: _day_text,
            ATTR_ENTITY_PICTURE: f"/local/renoweb/{self._pickup_events.entity_picture}?{str(_current_date.timestamp())}",
            ATTR_LAST_UPDATE: self._pickup_events.last_updated,
            ATTR_NAME: self._pickup_events.friendly_name,
        }

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )

