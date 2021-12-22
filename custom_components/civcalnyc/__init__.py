"""The NYC Civil Service Calendar integration."""
from __future__ import annotations

import logging

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from civcalnyc.civcalapi import CivCalAPI

from .const import DOMAIN, STARTUP_MESSAGE

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NYC Civil Service Calendar from a config entry."""

    if DOMAIN not in hass.data:
        # Print startup message
        _LOGGER.info(STARTUP_MESSAGE)

    api = CivCalAPI(async_get_clientsession(hass), entry.data["api_key"])

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=api.get_calendar(
            calendars=[
                CivCalAPI.CalendarTypes.DAYS_AHEAD,
                CivCalAPI.CalendarTypes.NEXT_EXCEPTIONS,
            ],
            scrub=True,
        ),
        update_interval=timedelta(minutes=30),
    )

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
