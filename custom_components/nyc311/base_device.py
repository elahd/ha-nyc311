"""Base for NYC311 entities."""
from __future__ import annotations

from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from nyc311calendar import CalendarDayEntry

from .const import DOMAIN, SERVICE_ICONS


class BaseDevice(CoordinatorEntity):  # type: ignore
    """Base class for NYC311 entities."""

    _attr_device_info: DeviceInfo | None = {
        "identifiers": {(DOMAIN, "NYC 311 Public API")}
    }

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        calendar_entry: CalendarDayEntry,
    ):
        """Initialize base device."""
        super().__init__(coordinator)

        self.coordinator = coordinator
        self._calendar_entry = calendar_entry

        if not self.extra_state_attributes:
            self._attr_extra_state_attributes: dict = {}

    def _get_icon(self, active_exception: bool) -> str:
        """Get icon for a given service / state."""
        return (
            f"{SERVICE_ICONS[self._calendar_entry.service_profile.service_type]}{'' if active_exception else '-off'}"
        )

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        await super().async_added_to_hass()

        self.update_device_data()

    @callback  # type: ignore
    def _handle_coordinator_update(self) -> None:
        """Update the entity with new REST API data."""

        self.update_device_data()

        reason = self._calendar_entry.exception_reason

        self._attr_extra_state_attributes.update(
            {
                "reason": reason if reason else None,
                "description": self._calendar_entry.status_profile.description,
                "status": self._calendar_entry.status_profile.standardized_type.name.title().replace(
                    "_", " "
                ),
            }
        )

        # If we use dict() here instead of a comprehension (as pylint requests), the dict won't actually sort.
        self._attr_extra_state_attributes = (
            {  # pylint: disable=unnecessary-comprehension
                key: value
                for key, value in sorted(
                    self._attr_extra_state_attributes.items(),
                    key=lambda item: str(item[0]),
                )
            }
        )

        self.async_write_ha_state()

    @callback  # type: ignore
    def update_device_data(self) -> None:
        """Update the entity when new data comes from the REST API."""
        raise NotImplementedError()
