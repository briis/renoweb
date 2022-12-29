"""The RenoWeb integration models."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pyrenoweb import RenoWeb


@dataclass
class RenoWebEntryData:
    """Data for the weatherflow integration."""

    renoweb: RenoWeb
    coordinator: DataUpdateCoordinator
    municipality_id: str
    address_id: str
