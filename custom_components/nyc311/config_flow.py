"""Config flow for NYC 311 Public Services Calendar integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from nyc311calendar import CalendarType
from nyc311calendar import NYC311API
import voluptuous as vol

from .const import DOMAIN
from .const import INTEGRATION_NAME

log = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required("api_key"): str})


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    api = NYC311API(async_get_clientsession(hass), data["api_key"])

    try:
        await api.get_calendar([CalendarType.NEXT_EXCEPTIONS])
    except NYC311API.InvalidAuth as error:
        raise InvalidAuth from error
    except NYC311API.CannotConnect as error:
        raise CannotConnect from error

    # Return info that you want to store in the config entry.
    # return {"api_key": data["api_key"]}
    log.debug("CivCalNYC successful authentication.")

    return {"title": INTEGRATION_NAME}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore
    """Handle a config flow for NYC 311 Public Services Calendar."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""

        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                log.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):  # type: ignore
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):  # type: ignore
    """Error to indicate there is invalid auth."""
