"""Shared Entity Definition for RenoWeb Integration."""
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.entity import Entity

from .const import DOMAIN


class RenoWebEntity(Entity):
    """Base class for RenoWeb Entities."""

    def __init__(self, renoweb, entity_object):
        """Initialize the entity."""
        super().__init__()
        self.renoweb = renoweb
        self.entity_object = entity_object

    @property
    def should_poll(self):
        """Poll entity to update attributes."""
        return False
