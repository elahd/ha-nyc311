from datetime import date, datetime
import logging

from homeassistant import core
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

import re
from civcalnyc.civcalapi import CivCalAPI

from .const import DOMAIN, DAY_NAMES
from .util import get_icon

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: core.HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
    discovery_info=None,
):
    """Setup the binary sensor platform."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Add days ahead sensors. One sensor per service per day for 8 days = 24 sensors!
    async_add_entities(
        (
            CivCalNYC_DaysAheadSensor(
                coordinator, day_delta, day_dict["date"], svc, attrs
            )
            for day_delta, day_dict in coordinator.data[
                CivCalAPI.CalendarTypes.DAYS_AHEAD
            ].items()
            for svc, attrs in day_dict["services"].items()
        ),
        True,
    )


async def async_setup_entry(
    hass: core.HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
    discovery_info=None,
):
    """Set up the config entry."""
    await async_setup_platform(hass, entry, async_add_entities, discovery_info=None)


class CivCalNYC_DaysAheadSensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        day_delta: int,
        day_date: date,
        service: CivCalAPI.ServiceType,
        attrs: dict,
    ):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._delta: int = day_delta
        self._svc: CivCalAPI.ServiceType = service
        self._date: date = day_date
        self._attrs = self.parse_attrs(attrs)
        # Set name here to lock in entity ID with _in_x_days suffix.
        self._name = "NYC311 {0}".format(
            self.generate_name(self._attrs["service_name"], self._delta, self._date)
        )

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, "NYC 311 Public API")}}

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return get_icon(
            self._svc, self._attrs["is_exception"] or self._attrs["routine_closure"]
        )

    @property
    def device_class(self):
        """Return the device class."""
        return "running"

    @property
    def unique_id(self):
        """Return the entity id of the sensor."""
        return re.sub(
            " ",
            "_",
            self.generate_name(self._attrs["service_name"], self._delta, self._date),
        ).lower()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def force_update(self):
        """Return the name of the sensor."""
        return True

    @property
    def is_on(self):
        """Return the state of the sensor."""

        data = self.coordinator.data[CivCalAPI.CalendarTypes.DAYS_AHEAD][self._delta]
        self._attrs = self.parse_attrs(data["services"][self._svc])
        self._date = data["date"]

        # Set entity name in "Wednesday" format instead of "in_3_days" format on an ongoing basis.
        # Entity ID will stay in predictable "in_3_days" format.
        self._name = self.generate_name(
            self._attrs["service_name"], self._delta, self._date, True
        )
        return (not self._attrs["is_exception"]) or (not self._attrs["routine_closure"])

    @property
    def extra_state_attributes(self):
        return self._attrs

    def parse_attrs(self, data):
        return {
            "reason": data["exception_reason"],
            "description": data["description"],
            "status": data["status_name"],
            "is_exception": data["is_exception"],
            "routine_closure": data["routine_closure"],
            "service_name": data["service_name"],
        }

    def generate_name(
        self, svc_name: str, delta: int, day_date: date, day_of_week_fmt: bool = False
    ):
        if day_of_week_fmt and delta > 1:
            day_name = datetime.combine(day_date, datetime.min.time()).strftime("on %A")
        else:
            day_name = DAY_NAMES[delta]
        return "{0} {1}".format(svc_name, day_name)
