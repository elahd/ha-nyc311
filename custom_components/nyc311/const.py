"""Constants for the NYC 311 Calendar integration."""

from civcalnyc.civcalapi import CivCalAPI

DOMAIN = "nyc311"
ISSUE_URL = "https://github.com/elahd/hass-nyc311/issues"

STARTUP_MESSAGE = f"""
===================================================================
 @@@@    *@@@ ,@@@     @@@   ,@@@@@@@@
@@@@@@@  @@@@@@@@@@   @@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@ @@@@@@@@@@@ @@@@@
@@@@@ @@@@@@@@    @@@@@    @@@@@@@@@@@@@
@@@@@   &@@@@@    @@@@@     %@@@@@@@@@@

{DOMAIN}
This is a custom component
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
===================================================================
"""

SERVICE_ICONS = {
    CivCalAPI.ServiceType.PARKING: "mdi:car-off",
    CivCalAPI.ServiceType.SCHOOL: "mdi:bag-personal-off",
    CivCalAPI.ServiceType.TRASH: "mdi:delete-off",
}
