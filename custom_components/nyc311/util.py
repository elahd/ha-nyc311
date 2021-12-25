"""Utility functions."""
from .const import SERVICE_ICONS
from civcalnyc.civcalapi import CivCalAPI


def get_icon(svc_id: CivCalAPI.ServiceType, is_closed: bool):
    return "{0}{1}".format(SERVICE_ICONS[svc_id], "-off" if is_closed else "")
