"""Implements 'Next Exception' sensors."""
from __future__ import annotations

import logging
import re

from homeassistant import core
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from nyc311calendar import CalendarDayEntry, CalendarType

from .base_device import BaseDevice
from .const import DOMAIN

log = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,  # pylint: disable=unused-argument
    discovery_info: DiscoveryInfoType | None = None,  # pylint: disable=unused-argument
) -> None:
    """Set up entities using the sensor platform from this config entry."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Add next exception sensors
    async_add_entities(
        (
            NextExceptionSensor(coordinator=coordinator, calendar_entry=calendar_entry)
            for calendar_entry in coordinator.data[
                CalendarType.NEXT_EXCEPTIONS
            ].values()
        ),
        True,
    )


class NextExceptionSensor(BaseDevice, SensorEntity):  # type: ignore
    """Next Exception sensor."""

    _attr_device_class = SensorDeviceClass.DATE

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        calendar_entry: CalendarDayEntry,
    ):
        """Initialize next exception sensor."""
        super().__init__(coordinator=coordinator, calendar_entry=calendar_entry)

        self._attr_name = (
            "Next"
            f" {self._calendar_entry.service_profile.name} {self._calendar_entry.service_profile.exception_name}"
        )
        self._attr_unique_id = re.sub(" ", "_", self._attr_name).lower()

    def update_device_data(self) -> None:
        """Update the entity when coordinator is updated."""
        self._calendar_entry: CalendarDayEntry = self.coordinator.data[
            CalendarType.NEXT_EXCEPTIONS
        ][self._calendar_entry.service_profile.service_type]

        self._attr_extra_state_attributes.update(
            {
                "closure_type": "Exception",
            }
        )

        self._attr_native_value = self._calendar_entry.date

        self._attr_icon = self._get_icon(self._attr_state)
