"""The NYC 311 Public Services Calendar integration."""
from __future__ import annotations

from datetime import timedelta
import logging

import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from nyc311calendar import NYC311API, CalendarType

from .const import DOMAIN, INTEGRATION_NAME, STARTUP_MESSAGE

log = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor", "binary_sensor", "calendar"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NYC 311 Public Services Calendar from a config entry."""
    if DOMAIN not in hass.data:
        # Print startup message
        log.info(STARTUP_MESSAGE)

    # Load data for domain. If not present, initlaize dict for this domain.
    hass.data.setdefault(DOMAIN, {})

    api = NYC311API(async_get_clientsession(hass), entry.data["api_key"])

    async def async_update_data() -> bool | dict:
        """Get fresh data from API."""
        try:
            async with async_timeout.timeout(10):
                return dict(
                    await api.get_calendar(
                        [
                            CalendarType.WEEK_AHEAD,
                            CalendarType.NEXT_EXCEPTIONS,
                            CalendarType.QUARTER_AHEAD,
                        ],
                        scrub=True,
                    )
                )
        except NYC311API.InvalidAuth as err:
            raise ConfigEntryAuthFailed from err
        except NYC311API.CannotConnect as err:
            raise UpdateFailed("Error communicating with API.") from err

    coordinator = DataUpdateCoordinator(
        hass,
        log,
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

    hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return bool(unload_ok)
