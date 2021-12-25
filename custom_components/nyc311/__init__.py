"""The NYC 311 Public Services Calendar integration."""
from __future__ import annotations

from datetime import timedelta
import logging

import async_timeout
from civcalnyc.civcalapi import CivCalAPI

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, INTEGRATION_NAME, STARTUP_MESSAGE

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor", "binary_sensor"]


async def async_setup(hass: HomeAssistantType, config: dict):
    """Set up the NYC 311 Public Services Calendar component."""

    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NYC 311 Public Services Calendar from a config entry."""

    if DOMAIN not in hass.data:
        # Print startup message
        _LOGGER.info(STARTUP_MESSAGE)

    api = CivCalAPI(async_get_clientsession(hass), entry.data["api_key"])

    async def async_update_data():
        try:
            async with async_timeout.timeout(10):
                return await api.get_calendar(
                    [
                        CivCalAPI.CalendarTypes.DAYS_AHEAD,
                        CivCalAPI.CalendarTypes.NEXT_EXCEPTIONS,
                    ],
                    scrub=True,
                )
        except CivCalAPI.InvalidAuth as err:
            raise ConfigEntryAuthFailed from err
        except CivCalAPI.CannotConnect as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(minutes=30),
    )

    device_registry = dr.async_get(hass)

    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, "NYC 311 Public API")},
        manufacturer="The City of New York",
        name=INTEGRATION_NAME,
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
