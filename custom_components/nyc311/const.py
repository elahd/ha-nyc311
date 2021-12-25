"""Constants for the NYC 311 Calendar integration."""

from nyc311calendar.api import NYC311API

DOMAIN = "nyc311"
ISSUE_URL = "https://github.com/elahd/hass-nyc311/issues"
INTEGRATION_NAME = "NYC 311 Public Services Calendar"

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
    NYC311API.ServiceType.PARKING: "mdi:car",
    NYC311API.ServiceType.SCHOOL: "mdi:bag-personal",
    NYC311API.ServiceType.TRASH: "mdi:delete",
}

DAY_NAMES = {
    -1: "Yesterday",
    0: "Today",
    1: "Tomorrow",
    2: "in 2 Days",
    3: "in 3 Days",
    4: "in 4 Days",
    5: "in 5 Days",
    6: "in 6 Days",
}
