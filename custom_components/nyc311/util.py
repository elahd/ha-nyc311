"""Utility functions."""
from .const import SERVICE_ICONS
from nyc311calendar.api import NYC311API


def get_icon(svc_id: NYC311API.ServiceType, is_closed: bool):
    return "{0}{1}".format(SERVICE_ICONS[svc_id], "-off" if is_closed else "")
