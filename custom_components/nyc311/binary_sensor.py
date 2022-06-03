"""Binary sensor API entity."""
from __future__ import annotations

from datetime import date
from datetime import datetime
import logging
from typing import Literal

from homeassistant import core
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity_platform import DiscoveryInfoType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from nyc311calendar import CalendarDayEntry
from nyc311calendar import CalendarType
from nyc311calendar.services import Service

from .base_device import BaseDevice
from .const import DAY_NAMES
from .const import DOMAIN

log = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,  # pylint: disable=unused-argument
    discovery_info: DiscoveryInfoType | None = None,  # pylint: disable=unused-argument
) -> None:
    """Set up entities using the binary sensor platform from this config entry."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Add days ahead sensors. One sensor per service per day for 8 days = 24 sensors!
    async_add_entities(
        (
            DaysAheadSensor(
                coordinator=coordinator,
                day_delta_from_today=day_delta_from_today,
                calendar_entry=calendar_entry,
            )
            for day_delta_from_today, day_attributes in coordinator.data[
                CalendarType.WEEK_AHEAD
            ].items()
            for calendar_entry in day_attributes["services"].values()
        ),
        True,
    )


class DaysAheadSensor(BaseDevice, BinarySensorEntity):  # type: ignore
    """Sensor showing exceptions over next few days."""

    NORMAL_EXCEPTIONS = [
        Service.StandardizedStatusType.REMOTE,
        Service.StandardizedStatusType.NORMAL_SUSPENDED,
        Service.StandardizedStatusType.NORMAL_ACTIVE,
    ]

    _attr_device_info: DeviceInfo | None = {
        "identifiers": {(DOMAIN, "NYC 311 Public API")}
    }

    _attr_force_update = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        day_delta_from_today: int,
        calendar_entry: CalendarDayEntry,
    ):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator=coordinator, calendar_entry=calendar_entry)

        self._delta_from_today: int = day_delta_from_today

        # Set name here to lock in entity ID with _in_x_days suffix.
        self._attr_name = f"NYC311 {self._generate_name(service_name=calendar_entry.service_profile.name,delta_from_today=self._delta_from_today,calendar_entry_date=calendar_entry.date)}"

        self._attr_unique_id = (
            self._generate_name(
                service_name=calendar_entry.service_profile.name,
                delta_from_today=self._delta_from_today,
                calendar_entry_date=calendar_entry.date,
            )
            .lower()
            .replace(" ", "_")
        )

    def update_device_data(self) -> None:
        """Update the entity when coordinator is updated."""

        self._calendar_entry: CalendarDayEntry = self.coordinator.data[
            CalendarType.WEEK_AHEAD
        ][self._delta_from_today]["services"][
            self._calendar_entry.service_profile.service_type
        ]

        # Set entity name in "Wednesday" format instead of "in_3_days" format on an ongoing basis.
        # Entity ID will stay in predictable "in_3_days" format.

        self._attr_name = self._generate_name(
            calendar_entry_date=self._calendar_entry.date,
            service_name=self._calendar_entry.service_profile.name,
            delta_from_today=self._delta_from_today,
            day_of_week_fmt=True,
        )

        closure_type: Literal["Routine"] | Literal["Exception"] | None
        if (
            self._calendar_entry.status_profile.standardized_type
            == Service.StandardizedStatusType.NORMAL_ACTIVE
        ):
            closure_type = None
        elif (
            self._calendar_entry.status_profile.standardized_type
            in self.NORMAL_EXCEPTIONS
        ):
            closure_type = "Routine"
        else:
            closure_type = "Exception"

        self._attr_extra_state_attributes.update(
            {
                "service_name": self._calendar_entry.service_profile.name,
                "closure_type": closure_type,
                "date": self._calendar_entry.date.isoformat(),
            }
        )

        self._attr_is_on = (
            self._calendar_entry.status_profile.standardized_type
            not in self.NORMAL_EXCEPTIONS
        )

        self._attr_icon = self._get_icon(
            self._attr_extra_state_attributes["closure_type"] == "Exception",
        )

    @classmethod
    def _generate_name(
        cls,
        service_name: str,
        delta_from_today: int,
        calendar_entry_date: date,
        day_of_week_fmt: bool = False,  # True for name, False for unique ID.
    ) -> str:
        """Generate entity name and unique ID."""

        if day_of_week_fmt and delta_from_today > 1:
            # On Wednesday
            day_name = datetime.combine(
                calendar_entry_date, datetime.min.time()
            ).strftime("on %A")
        else:
            # In 3 days
            day_name = DAY_NAMES[delta_from_today]
        return f"{service_name} Exception {day_name}"
