"""Binary sensor calendar entity."""
from __future__ import annotations

import datetime
import logging

from homeassistant import core
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from nyc311calendar import CalendarDayEntry, CalendarType, GroupBy
from nyc311calendar.services import Service, ServiceType

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
            Calendar(
                coordinator=coordinator,
                service=service_type,
            )
            for service_type in ServiceType
        ),
        True,
    )


class Calendar(CalendarEntity, CoordinatorEntity):  # type: ignore
    """Calendar created on a per-service basis."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        service: ServiceType,
    ):
        """Initialize calendar."""
        super().__init__(coordinator)

        self.coordinator = coordinator
        self._service = service

        self._calendar: CalendarDayEntry = {}

        # Hack to pluralize NYC Schools
        self._attr_name = (
            "NYC Schools"
            if self._service is ServiceType.SCHOOL
            else f"NYC {self._service.name.title()}"
        )

        self._attr_unique_id = f"nyc311_{self._service.name.lower()}"

        self._attr_device_info: DeviceInfo | None = {
            "identifiers": {(DOMAIN, "NYC 311 Public API")}
        }

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""

        events = self._build_calendar(start_date=start_date, end_date=end_date)

        return events if isinstance(events, list) else []

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""

        event = self._build_calendar(next_event=True)

        return event if isinstance(event, CalendarEvent) else None

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        await super().async_added_to_hass()

        self.update_device_data()

    @callback  # type: ignore
    def _handle_coordinator_update(self) -> None:
        """Update the entity with new REST API data."""

        self.update_device_data()

        self.async_write_ha_state()

    @callback  # type: ignore
    def update_device_data(self) -> None:
        """Update the entity when new data comes from the API."""

        self._calendar = self.coordinator.data[CalendarType.QUARTER_AHEAD][
            GroupBy.SERVICE
        ][self._service]

    @callback  # type: ignore
    def _build_calendar(
        self,
        start_date: datetime.datetime | None = None,
        end_date: datetime.datetime | None = None,
        next_event: bool = False,
    ) -> list[CalendarEvent] | CalendarEvent:
        """Build HA-standard calendar."""

        # next_event: if true, returns the next exception for this calendar. if false, returns all exceptions between start and end date, exclusive.

        if (next_event and (start_date or end_date)) or (
            bool(start_date) ^ bool(end_date)
        ):
            raise ValueError

        calendar_events: list[CalendarEvent] = []

        for date_ in sorted(self._calendar):
            calendar_entry: CalendarDayEntry = self._calendar[date_]
            if (
                calendar_entry.status_profile.standardized_type
                in [
                    Service.StandardizedStatusType.NORMAL_ACTIVE,
                    Service.StandardizedStatusType.NORMAL_SUSPENDED,
                ]
            ) or (
                not next_event
                and start_date
                and end_date
                and (
                    (calendar_entry.date < start_date.date())
                    or (calendar_entry.date > end_date.date())
                )
            ):
                continue

            calendar_event = CalendarEvent(
                start=calendar_entry.date,
                end=calendar_entry.date,
                summary=calendar_entry.exception_summary,
                description=calendar_entry.raw_description,
            )

            if next_event:
                return calendar_event

            calendar_events.append(calendar_event)

        return calendar_events
