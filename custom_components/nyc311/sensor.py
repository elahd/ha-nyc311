import logging

from homeassistant import core
from homeassistant.const import DEVICE_CLASS_DATE
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

import re
from civcalnyc.civcalapi import CivCalAPI

from .const import DOMAIN, SERVICE_ICONS

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: core.HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
    discovery_info=None,
):
    """Setup the sensor platform."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Add date sensors
    async_add_entities(
        CivCalNYC_NextExceptionSensor(coordinator, next_exc_svc, next_exc_data)
        for next_exc_svc, next_exc_data in coordinator.data[
            CivCalAPI.CalendarTypes.NEXT_EXCEPTIONS
        ].items()
    )


async def async_setup_entry(
    hass: core.HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
    discovery_info=None,
):
    """Set up the config entry."""
    await async_setup_platform(hass, entry, async_add_entities, discovery_info=None)


class CivCalNYC_NextExceptionSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        exc_svc: CivCalAPI.ServiceType,
        exc_data: dict,
    ):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._exc_svc = exc_svc
        self._sensor_name = "Next {0} {1}".format(
            exc_data["service_name"], exc_data["exception_name"]
        )
        self._unique_id = "sensor.{0}".format(
            re.sub(" ", "_", self._sensor_name)
        ).lower()
        self._sensor_icon = SERVICE_ICONS[self._exc_svc]

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return self._sensor_icon

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_DATE

    @property
    def unique_id(self):
        """Return the entity id of the sensor."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._sensor_name

    @property
    def state(self):
        """Return the state of the sensor."""

        this_exc_data = self.coordinator.data[CivCalAPI.CalendarTypes.NEXT_EXCEPTIONS][
            self._exc_svc
        ]

        self._attrs = {
            "reason": this_exc_data["exception_reason"],
            "description": this_exc_data["description"],
            "status": this_exc_data["status_name"],
        }
        return this_exc_data["date"].isoformat()

    @property
    def extra_state_attributes(self):
        return self._attrs

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._unique_id
